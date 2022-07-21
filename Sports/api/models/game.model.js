const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const GameSchema = new Schema({
    name: { type: String },
    shots: { type: Number },
    goals: { type: Number },
    points: { type: Number},
    assists: { type: Number },
    saves: { type: Number },
    fouls: { type: Number},
    steals: {type:Number}
});

const Game = mongoose.model('Game', GameSchema);
module.exports = Game;