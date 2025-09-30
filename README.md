# Game Controls

From the [challenge site](https://berghain.challenges.listenlabs.ai/)

### Create a new game:
```
    /new-game?scenario=1&playerId=<playerId>

    {
      "gameId": UUID,
      "constraints": {
        "attribute": AttributeId,
        "minCount": number
      }[],
      "attributeStatistics": {
        "relativeFrequencies": {
          [attributeId]: number // 0.0-1.0
        },
        "correlations": {
          [attributeId1]: {
            [attributeId2]: number // -1.0-1.0
          }
        }
      }
    }
```

### Get person and make decision
```
    /decide-and-next?gameId=uuid&personIndex=0&accept=true

    Get the next person in the queue.
    For the first person (personIndex=0), the accept parameter
    is optional. For subsequent persons, include accept=true
    or accept=false to make a decision.

    {
      "status": "running",
      "admittedCount": number,
      "rejectedCount": number,
      "nextPerson": {
        "personIndex": number,
        "attributes": { [attributeId]: boolean }
      }
    } | {
      "status": "completed",
      "rejectedCount": number,
      "nextPerson": null
    } | {
      "status": "failed",
      "reason": string,
      "nextPerson": null
    }
```
