var fs = require('fs');
var haversine = require('haversine');
var moment = require('moment');
//moment().format();

fs.readFile('sample_worlds.json', 'utf8', function (error, fileWorld) {	
	fs.readFile('sample_user.json', 'utf8', function(error, fileUser){
		user = JSON.parse(fileUser)['user'];
		worlds = JSON.parse(fileWorld)['data'];
		
		activeWorlds = [];
		userDateTime = moment(user['usertime']);
		for (i = 0; i < worlds.length; i++) { 
			if (worlds[i]['time']['timestart']) {
				worldStart = moment((worlds[i]['time']['timestart']));
				worldEnd = moment((worlds[i]['time']['timeend']));
				if (worldStart < userDateTime && worldEnd > userDateTime) {
					activeWorlds.push(worlds[i]);
				}
			}
			else {
				activeWorlds.push(worlds[i]);
			};
		}

		withinWorlds = [];
		userLat = user["userloc"]["coordinates"][0];
		userLong = user["userloc"]["coordinates"][1];
		for (i = 0; i < activeWorlds.length; i++) { 
			worldLat = activeWorlds[i]["loc"]["coordinates"][0];
			worldLong = activeWorlds[i]["loc"]["coordinates"][1];
			worldRadius = activeWorlds[i]["radius"];
			distance = haversine({latitude: userLat, longitude: userLong}, {latitude: worldLat, longitude: worldLong})  * 1000;
			if (distance < worldRadius) {
				withinWorlds.push(activeWorlds[i])
			};
		};

		worldswTagCount = [];
		for (i = 0; i < withinWorlds.length; i++) {
			count = 0;
			for (x=0; x < withinWorlds[i]["tags"].length; x++) {
				for (y = 0; y < user['tags'].length; y++) {
					if (withinWorlds[i]["tags"][x] === user['tags'][y]) {
						count += 1;
					};
				};
			};
		withinWorlds[i]['sharedTagCount'] = count;
		worldswTagCount.push(withinWorlds[i]);
		};


		function sortFunction(a, b){
			return(b['sharedTagCount'] - a['sharedTagCount']);
		}
		console.log(worldswTagCount.sort(sortFunction));
		return worldswTagCount.sort(sortFunction);

	});
});
