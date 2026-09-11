param location string
param workspaceResourceId string
param actionGroupResourceId string

var completionQuery = '''
customEvents
| where name in ('job_queue_accepted', 'job_processing_completed')
| extend jobId = tostring(customDimensions.jobId)
| summarize acceptedAt = minif(timestamp, name == 'job_queue_accepted'), completedAt = maxif(timestamp, name == 'job_processing_completed') by jobId
| where isnotnull(acceptedAt) and isnotnull(completedAt)
| extend durationMinutes = datetime_diff('second', completedAt, acceptedAt) / 60.0
| summarize completionRate = 100.0 * countif(durationMinutes <= 10) / count()
| extend Breach = iff(completionRate < 95, 1, 0)
'''

resource completionAlert 'Microsoft.Insights/scheduledQueryRules@2021-08-01' = {
  name: 'processing-completion-slo'
  location: location
  properties: {
    description: 'Fewer than 95 percent of queue-accepted jobs complete within ten minutes.'
    enabled: true
    severity: 2
    scopes: [ workspaceResourceId ]
    evaluationFrequency: 'PT15M'
    windowSize: 'PT1H'
    criteria: {
      allOf: [
        {
          query: completionQuery
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

resource completionWorkbook 'Microsoft.Insights/workbooks@2023-06-01' = {
  name: guid(workspaceResourceId, 'processing-completion-performance')
  location: location
  kind: 'shared'
  properties: {
    displayName: 'Processing completion performance'
    serializedData: string({ version: 'Notebook/1.0', items: [] })
    version: '1.0'
    category: 'workbook'
    sourceId: workspaceResourceId
  }
}
