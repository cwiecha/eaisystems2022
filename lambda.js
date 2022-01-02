var AWS = require('aws-sdk');
AWS.config.update({region: 'us-west-2'});
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

const http = require('http');

function sqsWrite(params, callbk) {
    console.log('In sqsWrite, params: ' + params );
    sqs.sendMessage(params, function(err, data) {
    if (err) {
        console.log("Error", err);
    } else {
        console.log("Success", data.MessageId);
    }
});
}

exports.handler = (event, context, callback) => {

    event.Records.forEach((record) => {
        var record_str = JSON.stringify(record, null, 2);
        console.log('Stream record: ', record_str);
        console.log('incoming ')

        if (record.eventName == 'INSERT') {
            // callAPI("rows/all", result => console.log(result))

            var params = {
             // Remove DelaySeconds parameter and value for FIFO queues
                MessageAttributes: {
                    "MyLabel": {
                     DataType: "String",
                     StringValue: "Test attribute"
                    }
                },
                MessageBody: record.dynamodb.NewImage.msg.S,
                QueueUrl: "<your queue url>"
            };

            sqsWrite(params, result => console.log(result));
        }
    });


    callback(null, `Successfully processed ${event.Records.length} records.`);
};
