const { authJwt } = require("../middlewares");
const controller = require("../controllers/sport.controller");

module.exports = function(app) {
    app.use(function(req, res, next) {
        res.header(
        "Access-Control-Allow-Headers",
        "x-access-token, Origin, Content-Type, Accept"
        );
        next();
    });

    // Fetch all stats and game history
    app.get("/api/stats", [authJwt.verifyToken], controller.fetchStats);

    // Add a game and stats
    app.post("/api/game",[authJwt.verifyToken], controller.saveGame);

};
