(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["three-man-weave"] = {
    id: "three-man-weave",
    title: "Three-Player Weave",
    titleLines: ["Three-Player", "Weave"],
    status: "ready",
    categories: ["Passing", "Transition"],
    summary: "Three players pass ahead and exchange lanes, with each receiver carrying the ball behind the passer into the middle lane.",
    variations: [
      "Players can wait at the far end while the remaining groups come down the court, then return in the opposite direction. The next group may start when the previous group crosses half court.",
      "Specify the type of pass players must use."
    ],
    pointsOfEmphasis: [
      "Sprint down the court.",
      "Run wide and fill the lanes.",
      "Communicate and call for the ball.",
      "Pass in front of the moving receiver.",
      "Do not travel.",
      "Keep the ball off the floor."
    ],
    equipment: { players: 3, basketballs: 1 },
    court: {
      type: "full",
      asset: "assets/courts/basketball-fullcourt.svg",
      aspectRatio: "5 / 3",
      label: "Full court",
      startingEnd: "left"
    },
    players: [
      { id: "1", label: "1", team: "offense" },
      { id: "2", label: "2", team: "offense" },
      { id: "3", label: "3", team: "offense" }
    ],
    steps: [
      {
        title: "Start in three lanes",
        description: "Form three lines on the baseline. Player 1 begins in the middle with the ball.",
        focus: 5,
        ball: "1",
        positions: { "1": [5, 50], "2": [5, 29], "3": [5, 71] },
        movements: []
      },
      {
        title: "Pass, then exchange lanes",
        description: "All three players advance as Player 1 passes to Player 2. Player 1 then crosses ahead into the outside lane while Player 2 carries the ball into the middle and Player 3 continues up the court.",
        focus: 29,
        ball: "2",
        ballPosition: [27, 50],
        duration: 3000,
        positions: { "1": [32, 29], "2": [27, 50], "3": [27, 71] },
        ballPath: [
          { position: [5, 50], offset: 0, layer: "over" },
          { position: [15, 29], offset: 0.4, layer: "over" },
          { position: [15, 29], offset: 0.52, layer: "over" },
          { position: [21, 40], offset: 0.76, layer: "over" },
          { position: [27, 50], offset: 1, layer: "over" }
        ],
        movements: [
          { player: "1", path: "curve-via", points: [{ position: [5, 50], offset: 0 }, { position: [15, 50], offset: 0.4 }, { position: [24, 38], offset: 0.65 }, { position: [32, 29], offset: 1 }] },
          { player: "2", path: "curve-via", points: [{ position: [5, 29], offset: 0 }, { position: [15, 29], offset: 0.4 }, { position: [15, 29], offset: 0.52 }, { position: [21, 40], offset: 0.76 }, { position: [27, 50], offset: 1 }] },
          { player: "3", path: "curve-via", points: [{ position: [5, 71], offset: 0 }, { position: [15, 71], offset: 0.4 }, { position: [27, 71], offset: 1 }] }
        ]
      },
      {
        title: "Pass and exchange again",
        description: "All three players advance as Player 2 passes to Player 3. Player 2 then crosses ahead into the outside lane while Player 3 carries the ball into the middle and Player 1 continues up the court.",
        focus: 52,
        ball: "3",
        ballPosition: [51, 50],
        duration: 3000,
        positions: { "1": [52, 29], "2": [56, 71], "3": [51, 50] },
        ballPath: [
          { position: [27, 50], offset: 0, layer: "over" },
          { position: [40, 71], offset: 0.4, layer: "over" },
          { position: [40, 71], offset: 0.52, layer: "over" },
          { position: [46, 61], offset: 0.76, layer: "over" },
          { position: [51, 50], offset: 1, layer: "over" }
        ],
        movements: [
          { player: "1", path: "curve-via", points: [{ position: [32, 29], offset: 0 }, { position: [40, 29], offset: 0.4 }, { position: [52, 29], offset: 1 }] },
          { player: "2", path: "curve-via", points: [{ position: [27, 50], offset: 0 }, { position: [40, 50], offset: 0.4 }, { position: [48, 62], offset: 0.65 }, { position: [56, 71], offset: 1 }] },
          { player: "3", path: "curve-via", points: [{ position: [27, 71], offset: 0 }, { position: [40, 71], offset: 0.4 }, { position: [40, 71], offset: 0.52 }, { position: [46, 61], offset: 0.76 }, { position: [51, 50], offset: 1 }] }
        ]
      },
      {
        title: "Finish at the rim",
        description: "All three players advance as Player 3 passes to Player 1. Player 3 crosses ahead into the outside lane while Player 1 carries the ball into the middle and attacks the basket.",
        focus: 84,
        ball: "1",
        ballPosition: [84, 50],
        duration: 3000,
        positions: { "1": [84, 50], "2": [82, 66], "3": [88, 34] },
        ballPath: [
          { position: [51, 50], offset: 0, layer: "over" },
          { position: [64, 29], offset: 0.4, layer: "over" },
          { position: [64, 29], offset: 0.52, layer: "over" },
          { position: [73, 39], offset: 0.76, layer: "over" },
          { position: [84, 50], offset: 1, layer: "over" }
        ],
        movements: [
          { player: "1", path: "curve-via", points: [{ position: [52, 29], offset: 0 }, { position: [64, 29], offset: 0.4 }, { position: [64, 29], offset: 0.52 }, { position: [73, 39], offset: 0.76 }, { position: [84, 50], offset: 1 }] },
          { player: "2", path: "curve-via", points: [{ position: [56, 71], offset: 0 }, { position: [66, 71], offset: 0.4 }, { position: [82, 66], offset: 1 }] },
          { player: "3", path: "curve-via", points: [{ position: [51, 50], offset: 0 }, { position: [64, 50], offset: 0.4 }, { position: [76, 41], offset: 0.65 }, { position: [88, 34], offset: 1 }] }
        ]
      }
    ]
  };
}());
