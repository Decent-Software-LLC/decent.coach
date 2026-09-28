(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["close-out-drill"] = {
    id: "close-out-drill",
    title: "Close Out Drill",
    titleLines: ["Close Out", "Drill"],
    status: "ready",
    categories: ["Defense", "Footwork"],
    summary: "Defenders close out four perimeter players, react to a jab step, and recover before rotating to the next assignment.",
    variations: [
      "Practice both bunny-hop and stutter-step closeout methods."
    ],
    pointsOfEmphasis: [
      "Maintain correct defensive stance and footwork.",
      "The defender calls ‘ball’ on every closeout.",
      "Offensive players use a proper triple-threat stance and correct jab-step footwork."
    ],
    equipment: { players: 8, basketballs: 0 },
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
      { id: "d1", label: "X1", team: "defense" },
      { id: "d2", label: "X2", team: "defense" },
      { id: "d3", label: "X3", team: "defense" },
      { id: "d4", label: "X4", team: "defense" }
    ],
    steps: [
      {
        title: "Set the four spots",
        description: "Four offensive players begin in triple-threat stance around the three-point line. The remaining players form the defensive line. No ball is used.",
        focus: 50,
        ball: null,
        positions: { o1: [83, 35], o2: [66, 68], o3: [34, 68], o4: [17, 35], d1: [50, 17], d2: [46, 2], d3: [50, 2], d4: [54, 2] },
        movements: []
      },
      {
        title: "Close out player 1",
        description: "X1 closes out Player 1 using a bunny hop or stutter step, calls “ball,” and finishes under control in a correct defensive stance.",
        focus: 75,
        ball: null,
        positions: { o1: [83, 35], o2: [66, 68], o3: [34, 68], o4: [17, 35], d1: [78, 35], d2: [50, 17], d3: [50, 2], d4: [54, 2] },
        movements: []
      },
      {
        title: "Recover to player 2",
        description: "Player 1 makes a varied one-step offensive move. X1 drop-steps in that direction, makes one quick slide, and recovers to the next assignment as X2 begins its closeout.",
        focus: 62,
        ball: null,
        positions: { o1: [83, 35], o2: [66, 68], o3: [34, 68], o4: [17, 35], d1: [59, 60], d2: [78, 35], d3: [50, 17], d4: [54, 2] },
        duration: 3000,
        movements: [{
          player: "d1",
          path: "curve-via",
          points: [
            { position: [78, 35], offset: 0 },
            { position: [64, 43], offset: 0.3 },
            { position: [54, 22], offset: 0.58 },
            { position: [59, 60], offset: 1 }
          ]
        }]
      },
      {
        title: "Rotate through three closeouts",
        description: "The defenders continue the closeout, drop-step, quick-slide, and recovery sequence at the next assignments while maintaining proper stance and communication.",
        focus: 48,
        ball: null,
        positions: { o1: [83, 35], o2: [66, 68], o3: [34, 68], o4: [17, 35], d1: [41, 60], d2: [59, 60], d3: [78, 35], d4: [50, 17] },
        duration: 3000,
        movements: [
          {
            player: "d1",
            path: "curve-via",
            points: [
              { position: [59, 60], offset: 0 },
              { position: [51.8, 25.6], offset: 0.58 },
              { position: [41, 60], offset: 1 }
            ]
          },
          {
            player: "d2",
            path: "curve-via",
            points: [
              { position: [78, 35], offset: 0 },
              { position: [64, 43], offset: 0.3 },
              { position: [54, 22], offset: 0.58 },
              { position: [59, 60], offset: 1 }
            ]
          }
        ]
      },
      {
        title: "Continue rotations and rotate offensive players",
        description: "Complete the closeout sequence, then rotate personnel. X1 joins the offensive group, each offensive player advances one station, and Player 4 joins the defensive line.",
        focus: 50,
        ball: null,
        positions: { o1: [66, 68], o2: [34, 68], o3: [17, 35], o4: [50, 17], d1: [83, 35], d2: [41, 60], d3: [59, 60], d4: [78, 35] },
        duration: 5000,
        teamChangeDelay: 5000,
        teams: { o1: "offense", o2: "offense", o3: "offense", o4: "defense", d1: "offense", d2: "defense", d3: "defense", d4: "defense" },
        movements: [
          {
            player: "d1",
            path: "curve-via",
            points: [
              { position: [41, 60], offset: 0 },
              { position: [48.2, 25.6], offset: 0.35 },
              { position: [25, 35], offset: 0.6 },
              { position: [83, 35], offset: 1 }
            ]
          },
          {
            player: "d2",
            path: "curve-via",
            points: [
              { position: [59, 60], offset: 0 },
              { position: [51.8, 25.6], offset: 0.35 },
              { position: [41, 60], offset: 0.6 },
              { position: [41, 60], offset: 1 }
            ]
          },
          {
            player: "d3",
            path: "curve-via",
            points: [
              { position: [78, 35], offset: 0 },
              { position: [64, 43], offset: 0.18 },
              { position: [54, 22], offset: 0.35 },
              { position: [59, 60], offset: 0.6 },
              { position: [59, 60], offset: 1 }
            ]
          },
          {
            player: "d4",
            path: "curve-via",
            points: [
              { position: [50, 17], offset: 0 },
              { position: [78, 35], offset: 0.6 },
              { position: [78, 35], offset: 1 }
            ]
          },
          {
            player: "o1",
            path: "curve-via",
            points: [
              { position: [83, 35], offset: 0 },
              { position: [83, 35], offset: 0.6 },
              { position: [66, 68], offset: 1 }
            ]
          },
          {
            player: "o2",
            path: "curve-via",
            points: [
              { position: [66, 68], offset: 0 },
              { position: [66, 68], offset: 0.6 },
              { position: [34, 68], offset: 1 }
            ]
          },
          {
            player: "o3",
            path: "curve-via",
            points: [
              { position: [34, 68], offset: 0 },
              { position: [34, 68], offset: 0.6 },
              { position: [17, 35], offset: 1 }
            ]
          },
          {
            player: "o4",
            path: "curve-via",
            points: [
              { position: [17, 35], offset: 0 },
              { position: [17, 35], offset: 0.6 },
              { position: [50, 17], offset: 1 }
            ]
          }
        ]
      }
    ]
  };
}());
