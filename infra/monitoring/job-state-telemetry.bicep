param location string
param workspaceResourceId string
param applicationInsightsName string
param actionGroupResourceId string

var freshnessQuery = '''
customEvents
| where name == 'job_state_changed'
| summarize latestStateChange = max(timestamp)
| extend Breach = iff(isnull(latestStateChange) or datetime_diff('second', now(), latestStateChange) > 60, 1, 0)
'''

var jobStateQuery = '''
customEvents
| where name == 'job_state_changed'
| project timestamp,
          jobId = tostring(customDimensions.jobId),
          state = tostring(customDimensions.state),
          retryCount = toint(customMeasurements.retryCount),
          failureReason = tostring(customDimensions.failureReason),
          correlationId = tostring(customDimensions.correlationId)
| order by timestamp desc
'''

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource telemetryDiagnosticSetting 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: applicationInsights
  name: 'job-state-telemetry'
  properties: {
    workspaceId: workspaceResourceId
    logs: [
      { category: 'AppTraces', enabled: true }
      { category: 'AppEvents', enabled: true }
    ]
  }
}

resource staleTelemetryAlert 'Microsoft.Insights/scheduledQueryRules@2021-08-01' = {
  name: 'job-state-telemetry-stale'
  location: location
  properties: {
    description: 'Job-state telemetry is older than sixty seconds. Payloads must contain state, retry count, sanitized reason, and correlation ID only.'
    enabled: true
    severity: 2
    scopes: [ workspaceResourceId ]
    evaluationFrequency: 'PT1M'
    windowSize: 'PT5M'
    criteria: {
      allOf: [
        {
          query: freshnessQuery
          timeAggregation: 'Maximum'
          metricMeasureColumn: 'Breach'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: { numberOfEvaluationPeriods: 1, minFailingPeriodsToAlert: 1 }
        }
      ]
    }
    actions: { actionGroups: [ actionGroupResourceId ] }
  }
}

resource jobStateWorkbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: guid(workspaceResourceId, 'job-state-telemetry')
  location: location
  kind: 'shared'
  properties: {
    displayName: 'Job state telemetry'
    serializedData: string({
      version: 'Notebook/1.0'
      items: [
        {
          type: 3
          name: 'job-state-query'
          content: {
            version: 'KqlItem/1.0'
            query: jobStateQuery
          }
        }
      ]
    })
    version: '1.0'
    category: 'workbook'
    sourceId: workspaceResourceId
  }
}
