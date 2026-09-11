param location string
param workspaceResourceId string
param operatorEmail string

var availabilityQuery = '''
let eligibleMaintenance = customEvents
| where name == 'maintenance_window'
| extend announcedAt = todatetime(customDimensions.announcedAt), startsAt = todatetime(customDimensions.startsAt), endsAt = todatetime(customDimensions.endsAt)
| where announcedAt <= startsAt - 24h
| project startsAt, endsAt;
requests
| where name == 'GET /health'
| where timestamp >= startofmonth(now())
| extend excluded = toscalar(eligibleMaintenance | where timestamp between (startsAt .. endsAt) | count) > 0
| where excluded == false
| summarize availabilityPercent = 100.0 * countif(success == true) / count()
| extend Breach = iff(availabilityPercent < 99.9, 1, 0)
'''

resource operatorActionGroup 'Microsoft.Insights/actionGroups@2023-01-01' = {
  name: 'availability-operators'
  location: 'global'
  properties: {
    groupShortName: 'availability'
    enabled: true
    emailReceivers: [
      {
        name: 'operations'
        emailAddress: operatorEmail
        useCommonAlertSchema: true
      }
    ]
  }
}

resource availabilityAlert 'Microsoft.Insights/scheduledQueryRules@2021-08-01' = {
  name: 'api-availability-slo'
  location: location
  properties: {
    description: 'API availability is below 99.9 percent after eligible announced maintenance is excluded.'
    enabled: true
    severity: 1
    scopes: [ workspaceResourceId ]
    evaluationFrequency: 'PT5M'
    windowSize: 'P1D'
    criteria: {
      allOf: [
        {
          query: availabilityQuery
          timeAggregation: 'Maximum'
          metricMeasureColumn: 'Breach'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: {
      actionGroups: [ operatorActionGroup.id ]
      customProperties: { runbook: 'Validate API and worker health, then assess active dependency incidents.' }
    }
  }
}

resource workerHealthAlert 'Microsoft.Insights/scheduledQueryRules@2021-08-01' = {
  name: 'worker-health-risk'
  location: location
  properties: {
    description: 'Worker revisions have not emitted a healthy heartbeat within five minutes.'
    enabled: true
    severity: 1
    scopes: [ workspaceResourceId ]
    evaluationFrequency: 'PT1M'
    windowSize: 'PT5M'
    criteria: {
      allOf: [
        {
          query: '''
customEvents
| where name == 'worker_health'
| summarize latestHeartbeat = max(timestamp) by workerRevision = tostring(customDimensions.workerRevision)
| extend Breach = iff(datetime_diff('second', now(), latestHeartbeat) > 300, 1, 0)
| summarize Breach = max(Breach)
'''
          timeAggregation: 'Maximum'
          metricMeasureColumn: 'Breach'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: {
      actionGroups: [ operatorActionGroup.id ]
      customProperties: { runbook: 'Investigate the unhealthy worker revision and dependent services.' }
    }
  }
}

resource availabilityWorkbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: guid(workspaceResourceId, 'service-availability')
  location: location
  kind: 'shared'
  properties: {
    displayName: 'Monthly API availability'
    serializedData: string({
      version: 'Notebook/1.0'
      items: [
        {
          type: 3
          name: 'monthly-api-availability'
          content: {
            version: 'KqlItem/1.0'
            query: availabilityQuery
          }
        }
      ]
    })
    version: '1.0'
    category: 'workbook'
    sourceId: workspaceResourceId
  }
}
