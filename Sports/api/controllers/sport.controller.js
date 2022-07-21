const jwt = require("jsonwebtoken");
const db = require("../models");
const Sport = db.sport;
const Game = db.game;

module.exports.saveGame = async(req, res) => {
    try{
        let token = req.headers["x-access-token"];
        let currGame = new Game(req.body);
        currGame.save();
        jwt.verify(token, process.env.SECRET, (err,decoded) => {
            req.userId = decoded.id;
            Sport.findOne({userId:req.userId}).exec((err, sport) => {
                if (err) {
                    res.status(500).send({ message: err });
                    return;
                  }
            
                  if (!sport) {
                    return res.status(404).send({ message: "Account Not found." });
                  }
                sport.games.push(currGame);
                const old_game_len = sport.games.length -1;
                const game_len = sport.games.length;

                if(old_game_len > 0){
                    // Update stats
                    sport.totalScore = sport.totalScore+req.body.points;
                    sport.saves = ((sport.saves * old_game_len)+req.body.saves)/game_len;
                    sport.assists = ((sport.assists * old_game_len)+req.body.assists)/game_len;
                    sport.fouls = ((sport.fouls * old_game_len)+req.body.fouls)/game_len;
                    sport.steals = ((sport.steals * old_game_len)+req.body.steals)/game_len;
                    sport.accuracy = ((sport.accuracy * old_game_len)+(req.body.goals/req.body.shots))/game_len;
                    sport.average = sport.totalScore/game_len;
                }
                else{
                    sport.totalScore = req.body.points;
                    sport.saves =req.body.saves;
                    sport.assists = req.body.assists;
                    sport.fouls = req.body.fouls;
                    sport.steals = req.body.steals;
                    sport.accuracy = req.body.goals/req.body.shots;
                    sport.average = sport.totalScore;
                }
                sport.save();
                res.send({ message: "Game was successfully saved!" });
        });
    });

    } catch (error) {
        console.log('Save game error: ', error);
        res.status(400).send({ message: error });
    }
}

module.exports.fetchStats = async(req, res) => {
    try{
        let token = req.headers["x-access-token"];
        jwt.verify(token, process.env.SECRET, (err,decoded) => {
            req.userId = decoded.id;
            Sport.find({userId:req.userId}).populate("games", "-__v")
            .exec((err, sport) => {
                if (err) {
                    res.status(500).send({ message: err });
                    return;
                  }
            
                  if (!sport) {
                    return res.status(404).send({ message: "Account Not found." });
                  }

                  var gamers = [];
                  if(sport.games != undefined){
                    for (let i = 0; i < sport.games.length; i++) {
                        gamers.push("Game: " + sport.games[i].name.toUpperCase()+
                        ", shots: "+ sport.games[i].shots+
                        ", goals: "+ sport.games[i].goals+
                        ", points: "+ sport.games[i].points+
                        ", assists: "+ sport.games[i].assists+
                        ", saves: "+ sport.games[i].saves+
                        ", fouls: "+ sport.games[i].fouls+
                        ", steals: "+ sport.games[i].steals
                        );
                    }
                  
                  res.status(200).send({
                    id: sport._id,
                    userId: sport.userId,
                    name: sport.name,
                    sport: sport.sport,
                    accuracy: sport.accuracy,
                    saves: sport.saves,
                    average: sport.average,
                    assists: sport.assists,
                    totalScore: sport.totalScore,
                    fouls: sport.fouls,
                    steals: sport.steals,
                    games: gamers,
                    position: sport.position,
                    division: sport.division
                });
                }
                else{
                    res.status(200).send({sport});
                }
            });

        });
    } catch (error) {
        console.log('get stats error: ', error);
        res.status(400).send({ message: error });
    }
    }

