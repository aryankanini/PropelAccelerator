param location string
param workspaceResourceId string
param actionGroupResourceId string

var acknowledgementQuery = '''
customEvents
| where name == 'upload_acknowledged'
| extend acknowledgementMilliseconds = todouble(customMeasurements.acknowledgementMilliseconds)
| summarize acknowledgementP95 = percentile(acknowledgementMilliseconds, 95)
| extend Breach = iff(acknowledgementP95 > 2000, 1, 0)
'''

resource acknowledgementAlert 'Microsoft.Insights/scheduledQueryRules@2021-08-01' = {
  name: 'upload-acknowledgement-p95'
  location: location
  properties: {
    description: 'Upload acknowledgement p95 exceeds the two-second objective.'
    enabled: true
    severity: 2
    scopes: [
      workspaceResourceId
    ]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      allOf: [
        {
          query: acknowledgementQuery
          timeAggregation: 'Maximum'
          metricMeasureColumn: 'Breach'
          operator: 'GreaterThan'
          threshold: 0
          failingPeriods: {
            numberOfEvaluationPeriods: 1
            minFailingPeriodsToAlert: 1
          }
        }
      ]
    }
    actions: {
      actionGroups: [
        actionGroupResourceId
      ]
      customProperties: {
        runbook: 'Investigate API acknowledgement latency; queue delay is reported separately.'
      }
    }
  }
}

resource acknowledgementWorkbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: guid(workspaceResourceId, 'upload-acknowledgement-performance')
  location: location
  kind: 'shared'
  properties: {
    displayName: 'Upload acknowledgement performance'
    serializedData: string({ version: 'Notebook/1.0', items: [] })
    version: '1.0'
    category: 'workbook'
    sourceId: workspaceResourceId
  }
}
