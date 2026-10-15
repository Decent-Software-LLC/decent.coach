(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["shell-drill"] = {
    id: "shell-drill",
    title: "Shell Drill",
    titleLines: ["Shell Drill"],
    status: "ready",
    categories: ["Team Defense", "Positioning", "Communication"],
    summary: "Four defenders move together through on-ball pressure, deny, help, and split-line responsibilities as the offense moves the ball around the perimeter.",
    printPdf: "print/shell-drill.pdf",
    variations: [
      "Begin with stationary offense and allow every pass.",
      "Add V-cuts and replacements while the defense allows passes.",
      "Require defenders to deny passes after the movement is understood.",
      "Allow penetration so the defense must help and recover.",
      "Allow exchanges, then screens, before progressing to live four-on-four.",
      "Have high defenders sag against penetration instead of denying when that matches the team emphasis."
    ],
    pointsOfEmphasis: [
      "Jump to the ball as the pass is made - fly with the ball.",
      "See the ball and your player at the same time - point your pistols.",
      "Stay lower than the player you are guarding.",
      "Use correct slides, drop steps, and closeout footwork.",
      "Pressure passes and shots, stop penetration, and help teammates."
    ],
    equipment: { players: 8, basketballs: 1 },
    ballAbovePlayers: true,
    ballOffset: [-10, -10],
    mobileBallOffset: [-10, -10],
    court: {
      type: "half",
      asset: "assets/courts/basketball-halfcourt.svg",
      aspectRatio: "1090.86 / 912.61",
      label: "Half court",
      startingEnd: "bottom",
      rotation: 180
    },
    players: [
      { id: "o1", label: "1", team: "offense" },
      { id: "o2", label: "2", team: "offense" },
      { id: "o3", label: "3", team: "offense" },
      { id: "o4", label: "4", team: "offense" },
      { id: "d1", label: "X1", team: "defense" },
      { id: "d2", label: "X2", team: "defense" },
      { id: "d3", label: "X3", team: "defense" },
      { id: "d4", label: "X4", team: "defense" }
    ],
    steps: [
      {
        title: "Set the shell",
        description: "Place four offensive players at the guard and wing or corner spots. Match each player with a defender. Player 1 begins with the ball.",
        focus: 50,
        ball: "o1",
        callouts: { d1: "Ball", d2: "Deny", d3: "Deny", d4: "Help" },
        positions: { o1:[38,34],o2:[62,34],o3:[22,56],o4:[78,56],d1:[42,40],d2:[54,38],d3:[30,52],d4:[50,55] },
        movements: []
      },
      {
        title: "Fly with the first pass",
        description: "Player 1 passes to Player 2. Every defender moves while the ball is in the air: X2 closes to the ball, X1 denies the return pass, X4 denies the wing, and X3 drops into help.",
        focus: 54,
        ball: "o2",
        ballArrival: .5,
        callouts: { d1: "Deny", d2: "Ball", d3: "Help", d4: "Deny" },
        calloutDelays: { d1:1400, d2:1400, d3:1400, d4:1400 },
        duration: 2800,
        positions: { o1:[38,34],o2:[62,34],o3:[22,56],o4:[78,56],d1:[46,38],d2:[58,40],d3:[50,55],d4:[70,52] },
        movements: [
          { player:"d1",path:"curve-via",points:[{position:[42,40],offset:0},{position:[46,38],offset:1}] },
          { player:"d2",path:"curve-via",points:[{position:[54,38],offset:0},{position:[58,40],offset:1}] },
          { player:"d3",path:"curve-via",points:[{position:[30,52],offset:0},{position:[50,55],offset:1}] },
          { player:"d4",path:"curve-via",points:[{position:[50,55],offset:0},{position:[70,52],offset:1}] }
        ]
      },
      {
        title: "Shift to the wing",
        description: "Player 2 catches and faces, holds for the teaching count, then passes to Player 4. X4 closes out, X2 moves into deny position, and the weak-side defenders move into help and split-line positions.",
        focus: 62,
        ball: "o4",
        ballArrival: .5,
        callouts: { d1: "Split", d2: "Deny", d3: "Help", d4: "Ball" },
        calloutDelays: { d1:1500, d2:1500, d3:1500, d4:1500 },
        duration: 3000,
        positions: { o1:[38,34],o2:[62,34],o3:[22,56],o4:[78,56],d1:[50,52],d2:[67,46],d3:[47,56],d4:[72,60] },
        movements: [
          { player:"d1",path:"curve-via",points:[{position:[46,38],offset:0},{position:[50,52],offset:1}] },
          { player:"d2",path:"curve-via",points:[{position:[58,40],offset:0},{position:[67,46],offset:1}] },
          { player:"d3",path:"curve-via",points:[{position:[50,55],offset:0},{position:[47,56],offset:1}] },
          { player:"d4",path:"curve-via",points:[{position:[70,52],offset:0},{position:[72,60],offset:1}] }
        ]
      },
      {
        title: "Help across the shell",
        description: "The ball moves across to Player 3. X3 closes without allowing penetration, X1 denies the nearest pass, and X2 and X4 recover into help positions while seeing both ball and player.",
        focus: 42,
        ball: "o3",
        ballArrival: .55,
        callouts: { d1: "Deny", d2: "Help", d3: "Ball", d4: "Help" },
        calloutDelays: { d1:1760, d2:1760, d3:1760, d4:1760 },
        duration: 3200,
        positions: { o1:[38,34],o2:[62,34],o3:[22,56],o4:[78,56],d1:[33,46],d2:[50,52],d3:[28,60],d4:[53,56] },
        movements: [
          { player:"d1",path:"curve-via",points:[{position:[50,52],offset:0},{position:[33,46],offset:1}] },
          { player:"d2",path:"curve-via",points:[{position:[67,46],offset:0},{position:[50,52],offset:1}] },
          { player:"d3",path:"curve-via",points:[{position:[47,56],offset:0},{position:[28,60],offset:1}] },
          { player:"d4",path:"curve-via",points:[{position:[72,60],offset:0},{position:[53,56],offset:1}] }
        ]
      },
      {
        title: "Rotate and progress",
        description: "Rotate the offensive group to defense. Repeat the stationary passing stage until positioning is automatic, then add cuts, denial, penetration, exchanges, screens, and live four-on-four.",
        focus: 50,
        ball: "d1",
        ballArrival: .55,
        duration: 3200,
        teamChangeDelay: 2700,
        teams: { o1:"defense",o2:"defense",o3:"defense",o4:"defense",d1:"offense",d2:"offense",d3:"offense",d4:"offense" },
        positions: { o1:[42,40],o2:[54,38],o3:[30,52],o4:[50,55],d1:[38,34],d2:[62,34],d3:[22,56],d4:[78,56] },
        movements: [
          { player:"o1",path:"curve-via",points:[{position:[38,34],offset:0},{position:[42,40],offset:1}] },
          { player:"o2",path:"curve-via",points:[{position:[62,34],offset:0},{position:[54,38],offset:1}] },
          { player:"o3",path:"curve-via",points:[{position:[22,56],offset:0},{position:[30,52],offset:1}] },
          { player:"o4",path:"curve-via",points:[{position:[78,56],offset:0},{position:[50,55],offset:1}] },
          { player:"d1",path:"curve-via",points:[{position:[33,46],offset:0},{position:[38,34],offset:1}] },
          { player:"d2",path:"curve-via",points:[{position:[50,52],offset:0},{position:[62,34],offset:1}] },
          { player:"d3",path:"curve-via",points:[{position:[28,60],offset:0},{position:[22,56],offset:1}] },
          { player:"d4",path:"curve-via",points:[{position:[53,56],offset:0},{position:[78,56],offset:1}] }
        ]
      }
    ]
  };
}());
