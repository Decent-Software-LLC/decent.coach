(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["defensive-shuffle-and-pass"] = {
    id: "defensive-shuffle-and-pass", title: "Defensive Shuffle And Pass", titleLines: ["Defensive Shuffle", "And Pass"], status: "ready",
    categories: ["Defense", "Passing", "Footwork"],
    summary: "Three players combine crisp passing with repeated defensive shuffles between two ball-handlers.",
    variations: ["Specify the type of pass.", "Count the most completed passes in a set time."],
    pointsOfEmphasis: ["Use correct defensive footwork: wide, then wider.", "Deliver crisp, accurate passes."],
    equipment: { players: 3, basketballs: 2 },
    court: { type: "half", asset: "assets/courts/basketball-halfcourt.svg", aspectRatio: "1090.86 / 912.61", label: "Half court", startingEnd: "top" },
    players: [{ id: "p1", label: "1", team: "offense" }, { id: "p2", label: "2", team: "offense" }, { id: "p3", label: "3", team: "defense" }],
    steps: [
      { title: "Set up the triangle", description: "Two passers stand three to four steps apart. The worker begins opposite Player 1 in a low defensive stance.", focus: 50, ball: "p1", positions: { p1: [35, 72], p2: [65, 72], p3: [35, 42] }, movements: [] },
      { title: "Pass and return", description: "Player 1 passes to Player 3, who immediately returns a crisp pass while staying balanced and ready to move.", focus: 38, ball: "p1", duration: 2400, positions: { p1: [35, 72], p2: [65, 72], p3: [35, 42] }, ballPath: [{ position: [35,72], offset: 0 }, { position: [35,42], offset: .45 }, { position: [35,42], offset: .55 }, { position: [35,72], offset: 1 }], movements: [] },
      { title: "Shuffle to the second passer", description: "Player 3 stays low and shuffles wide-to-wider until positioned in front of Player 2.", focus: 50, ball: "p2", duration: 2400, positions: { p1: [35,72], p2: [65,72], p3: [65,42] }, movements: [{ player: "p3", path: "curve-via", points: [{ position: [35,42], offset: 0 }, { position: [45,38], offset: .35 }, { position: [55,46], offset: .7 }, { position: [65,42], offset: 1 }] }] },
      { title: "Return and repeat", description: "Player 2 passes to Player 3 and receives the return pass. Player 3 shuffles back toward Player 1 and the sequence continues.", focus: 50, ball: "p2", duration: 3000, positions: { p1: [35,72], p2: [65,72], p3: [35,42] }, ballPath: [{ position: [65,72], offset: 0 }, { position: [65,42], offset: .25 }, { position: [65,42], offset: .35 }, { position: [65,72], offset: .58 }, { position: [65,72], offset: 1 }], movements: [{ player: "p3", path: "curve-via", points: [{ position: [65,42], offset: 0 }, { position: [65,42], offset: .58 }, { position: [50,46], offset: .78 }, { position: [35,42], offset: 1 }] }] }
    ]
  };
}());
