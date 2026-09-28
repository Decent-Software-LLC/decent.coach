(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["bull-in-the-ring"] = {
    id: "bull-in-the-ring",
    title: "Bull In The Ring",
    titleLines: ["Bull In", "The Ring"],
    status: "ready",
    categories: ["Passing", "Defense"],
    summary: "Players pass across a circle while one defender pressures the ball and hunts for a touch or interception.",
    variations: [
      "Use two or more basketballs.",
      "Place two or more defenders inside the circle.",
      "Change the size of the circle to practice shorter or longer passes.",
      "Give the ball-handler a time limit to pass, such as a three-second count."
    ],
    pointsOfEmphasis: [
      "Fake a pass to make a pass.",
      "Apply tough on-ball pressure instead of sagging away.",
      "Keep active hands on defense.",
      "Do not throw soft, looping passes over the defender."
    ],
    equipment: { players: 9, playersLabel: "All Players", basketballs: 1 },
    court: {
      type: "half",
      asset: "assets/courts/basketball-halfcourt.svg",
      aspectRatio: "1090.86 / 912.61",
      label: "Half court",
      startingEnd: "top"
    },
    players: [
      { id: "o1", label: "1", team: "offense" },
      { id: "o2", label: "2", team: "offense" },
      { id: "o3", label: "3", team: "offense" },
      { id: "o4", label: "4", team: "offense" },
      { id: "o5", label: "5", team: "offense" },
      { id: "o6", label: "6", team: "offense" },
      { id: "o7", label: "7", team: "offense" },
      { id: "o8", label: "8", team: "offense" },
      { id: "d1", label: "X", team: "defense" }
    ],
    steps: [
      {
        title: "Form the ring",
        description: "Players form a wide circle around one defender. Player 1 begins with the ball, and passes may not go to an adjacent player.",
        focus: 50,
        ball: "o1",
        positions: { o1: [50, 24], o2: [33, 31], o3: [23, 47], o4: [29, 68], o5: [50, 78], o6: [71, 68], o7: [77, 47], o8: [67, 31], d1: [50, 50] },
        movements: []
      },
      {
        title: "Fake, pass, and pressure",
        description: "Player 1 uses a pass fake, then passes across the circle to Player 3. The defender pressures the ball and attacks the passing lane.",
        focus: 42,
        ball: "o3",
        ballArrival: 0.55,
        duration: 2600,
        positions: { o1: [50, 24], o2: [33, 31], o3: [23, 47], o4: [29, 68], o5: [50, 78], o6: [71, 68], o7: [77, 47], o8: [67, 31], d1: [39, 39] },
        movements: [
          { player: "d1", path: "curve-via", points: [{ position: [50, 50], offset: 0 }, { position: [50, 31], offset: 0.35 }, { position: [39, 39], offset: 1 }] }
        ]
      },
      {
        title: "Recover to the next pass",
        description: "Player 3 quickly passes across the circle to Player 6. The defender recovers, pressures the new ball-handler, and keeps active hands in the lane.",
        focus: 55,
        ball: "o6",
        ballArrival: 0.55,
        duration: 2600,
        positions: { o1: [50, 24], o2: [33, 31], o3: [23, 47], o4: [29, 68], o5: [50, 78], o6: [71, 68], o7: [77, 47], o8: [67, 31], d1: [50, 58] },
        movements: [
          { player: "d1", path: "curve-via", points: [{ position: [39, 39], offset: 0 }, { position: [31, 47], offset: 0.3 }, { position: [50, 58], offset: 1 }] }
        ]
      },
      {
        title: "Touch the pass and rotate",
        description: "The defender touches or intercepts the pass. The passer becomes the new defender, and the former defender joins the outside ring.",
        focus: 50,
        ball: "d1",
        ballPosition: [71, 68],
        duration: 3200,
        teamChangeDelay: 3000,
        teams: { o1: "offense", o2: "offense", o3: "offense", o4: "offense", o5: "offense", o6: "defense", o7: "offense", o8: "offense", d1: "offense" },
        positions: { o1: [50, 24], o2: [33, 31], o3: [23, 47], o4: [29, 68], o5: [50, 78], o6: [50, 50], o7: [77, 47], o8: [67, 31], d1: [71, 68] },
        ballPath: [
          { position: [71, 68], offset: 0, layer: "over" },
          { position: [50, 50], offset: 0.4, layer: "over" },
          { position: [50, 50], offset: 0.5, layer: "over" },
          { position: [71, 68], offset: 1, layer: "over" }
        ],
        movements: [
          { player: "d1", path: "curve-via", points: [{ position: [50, 58], offset: 0 }, { position: [50, 50], offset: 0.4 }, { position: [50, 50], offset: 0.5 }, { position: [71, 68], offset: 1 }] },
          { player: "o6", path: "curve-via", points: [{ position: [71, 68], offset: 0 }, { position: [71, 68], offset: 0.5 }, { position: [50, 50], offset: 1 }] }
        ]
      }
    ]
  };
}());
