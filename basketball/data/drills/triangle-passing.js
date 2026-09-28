(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["triangle-passing"] = {
    id: "triangle-passing",
    title: "Triangle Passing",
    titleLines: ["Triangle", "Passing"],
    status: "ready",
    categories: ["Passing", "Receiving"],
    summary: "Three half-court lines pass in sequence while receivers move to the ball and passers sprint to the end of the receiving line.",
    variations: [
      "Use two balls.",
      "Change direction and go anti-clockwise.",
      "On the coach’s vocal command, change direction during the drill."
    ],
    pointsOfEmphasis: [
      "Move to the ball to receive the pass.",
      "Show ten fingers and call the passer’s name.",
      "Sprint to the end of the line after passing."
    ],
    equipment: { players: 6, basketballs: 1 },
    court: {
      type: "half",
      asset: "assets/courts/basketball-halfcourt.svg",
      aspectRatio: "1090.86 / 912.61",
      label: "Half court",
      startingEnd: "top"
    },
    players: [
      { id: "p1", label: "1a", team: "offense" },
      { id: "p2", label: "2a", team: "offense" },
      { id: "p3", label: "3a", team: "offense" },
      { id: "p4", label: "1b", team: "offense" },
      { id: "p5", label: "2b", team: "offense" },
      { id: "p6", label: "3b", team: "offense" }
    ],
    steps: [
      {
        title: "Form three lines",
        description: "Use half-court. Form Line 1 and Line 3 at the half-court corners, with Line 2 underneath the basket. Player 2a starts with the ball.",
        focus: 50,
        ball: "p2",
        positions: { p1: [17, 86], p2: [50, 25], p3: [83, 86], p4: [17, 95], p5: [50, 14], p6: [83, 95] },
        movements: []
      },
      {
        title: "Move to the ball",
        description: "Player 1a moves to the ball and receives the pass from Player 2a. After passing, Player 2a sprints to the end of the line just passed to, and Player 1b advances.",
        focus: 45,
        ball: "p1",
        ballArrival: 0.5,
        duration: 3000,
        positions: { p1: [33.5, 86], p2: [17, 95], p3: [83, 86], p4: [17, 86], p5: [50, 14], p6: [83, 95] },
        movements: [
          { player: "p2", path: "staged", startOffset: 0.5 },
          { player: "p4", path: "staged", startOffset: 0.5 }
        ]
      },
      {
        title: "Pass to the next line",
        description: "Player 3a moves to the ball and receives the pass from Player 1a. After passing, Player 1a sprints to the end of the line just passed to, and Player 3b advances.",
        focus: 58,
        ball: "p3",
        ballPosition: [72.25, 67.25],
        ballArrival: 0.5,
        duration: 3000,
        positions: { p1: [83, 95], p2: [17, 95], p3: [74.75, 70.75], p4: [17, 86], p5: [50, 14], p6: [83, 86] },
        movements: [
          { player: "p1", path: "staged", startOffset: 0.5 },
          { player: "p6", path: "staged", startOffset: 0.5 }
        ]
      },
      {
        title: "Complete the triangle",
        description: "Player 2b moves to the ball and receives the pass from Player 3a. After passing, Player 3a sprints to the end of the line just passed to.",
        focus: 42,
        ball: "p5",
        ballArrival: 0.5,
        duration: 3000,
        positions: { p1: [83, 95], p2: [17, 95], p3: [50, 14], p4: [17, 86], p5: [41.75, 32], p6: [83, 86] },
        movements: [
          { player: "p3", path: "staged", startOffset: 0.5 }
        ]
      }
    ]
  };
}());
