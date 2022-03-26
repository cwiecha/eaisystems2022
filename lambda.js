var AWS = require('aws-sdk');
AWS.config.update({region: 'us-west-2'});
const docClient = new AWS.DynamoDB.DocumentClient();

async function createItem(params){
  try {
    await docClient.put(params).promise();
  } catch (err) {
    return err;
  }
}

exports.handler = (event, context, callback) => {

    event.Records.forEach( (record) => {
        var record_str = JSON.stringify(record, null, 2);
        console.log('Stream record: ', record_str);

        if (record.eventName == 'INSERT') {

            var params = {
                TableName : 'Lab4Logs',
                Item: {
                    "partition_key" : record.dynamodb.NewImage.partition_key.S,
                    "sort_key" : record.dynamodb.NewImage.sort_key.S,
                    "Class": record.dynamodb.NewImage.Class.S,
                    "Confidence": record.dynamodb.NewImage.Confidence.S,
                    "Label": record.dynamodb.NewImage.Label.S,
                    "Features": record.dynamodb.NewImage.Features.S
                }
            }
            createItem(params)
        }
    }),
    
    callback(null, `Successfully processed ${event.Records.length} records.`);
}
