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
                    "Probability": record.dynamodb.NewImage.Probability.S,
                    "Label": record.dynamodb.NewImage.Label.S,
                    "Features": record.dynamodb.NewImage.Features.S
                }
            };
            var int_class = parseInt(record.dynamodb.NewImage.Class.S);
            var float_probability = parseFloat(record.dynamodb.NewImage.Probability.S);
            var gap = 0;
            
            if ( int_class == 0 )
            {
                gap = float_probability;
            }
            else
            {
                gap = 1 - float_probability;
            };
            if ( gap > 0.25 )
               createItem(params)
        }
    }),
    
    callback(null, `Successfully processed ${event.Records.length} records.`);
}
