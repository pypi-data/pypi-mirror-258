var express = require('express');
var router = express.Router();
var bodyParser = require('body-parser')
var fetch = require('node-fetch')


var app = express()
var jsonParser = bodyParser.json()
const https = require('https');


const httpsAgent = new https.Agent({
  rejectUnauthorized: false,
});

router.post('/', jsonParser, function(req, res, next) {

   const input = req.body;
   console.log(input);
   
   const table = input.table 
   const action = input.action;
   const nodeid = input.nodeid;
   
  // let url = config.db.url + '/api/v2/table/' + table;
   let url = 'http://localhost:3011/data';
   
   try {
   
    	var response = { "nodes" : [], "edges": [] };
    	
    	switch (action) {
    	case "viewnode":
   	
			call(url + '/document/' + nodeid)
				.then( data => {
					response.nodes.push(data);
					res.json(response);
				});
			break;
		case "viewchild":
		

			call(url + '/edges.json' ) 	//'?condition={"$eq":{"source":"' + nodeid + '"}}' )
				.then( data => {
					return data.filter( d => d.source == nodeid );
				})
				.then( data => {
				 	response.edges = data;
					const nodeids = response.edges.map( d => d.target);
					console.log(nodeids);
					
					call( url + '/nodes.json' )		//'?condition={"$in":{"_id":[' + nodeids.toString() + ']}}' )
						.then( data1 => { 
							console.log(data1)
							response.nodes = data1.filter( d => nodeids.includes(d._id) );
							console.log(response.nodes)
							res.json(response);
						})

				})						
			break;
		default:
			console.log("action not defined: " + action)   
        }

   } catch (err) {
     console.log(err);
     res.status(500).send(err);
   }
});


async function call(url) {

	 result = await fetch(url, {
            method: 'GET',
          //  agent: httpsAgent,
            headers: {
              'Content-Type': 'application/json'
         //     'Authorization': 'Basic ' + Buffer.from('mapr:mapr').toString('base64')
            }
        })
        .then( (data) => { return data.json(); } )
        .catch(err => console.error(err));
        
    return result;
}



module.exports = router;
