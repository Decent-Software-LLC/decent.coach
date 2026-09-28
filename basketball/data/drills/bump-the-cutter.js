(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["bump-the-cutter"] = {
    id: "bump-the-cutter",
    title: "Bump The Cutter",
    titleLines: ["Bump The", "Cutter"],
    status: "ready",
    categories: ["Defense", "Denial"],
    summary: "A defender reads ball and cutter, meets the flash cut in the lane, and denies an easy catch in the key.",
    variations: [
      "Reposition the coach and cutter to different areas of the offensive half court."
    ],
    pointsOfEmphasis: [
      "Begin in the correct position relative to both ball and player.",
      "See both the ball and the player being guarded.",
      "Deny the pass inside the key.",
      "Make legal contact with the cutter using the chest or an arm bar.",
      "Use a high deny stance, then snap the head and arm down when the cutter goes low.",
      "Stay lower than the offensive player in a correct defensive stance.",
      "Use correct defensive footwork."
    ],
    equipment: { players: 3, basketballs: 1 },
    court: {
      type: "half",
      asset: "assets/courts/basketball-halfcourt.svg",
      aspectRatio: "1090.86 / 912.61",
      label: "Half court",
      startingEnd: "top"
    },
    players: [
      { id: "coach", label: "C", team: "neutral" },
      { id: "o1", label: "1", team: "offense" },
      { id: "d1", label: "X", team: "defense" }
    ],
    steps: [
      {
        title: "See ball and cutter",
        description: "The coach starts outside the three-point line with the ball. The cutter begins in the opposite corner, and the defender establishes a flat-triangle position in the key.",
        focus: 50,
        ball: "coach",
        positions: { coach: [80, 55], o1: [18, 24], d1: [50, 46] },
        movements: []
      },
      {
        title: "Meet the flash cut",
        description: "The offensive player flash-cuts toward the ball. The defender stays lower, meets the cutter in the lane, and makes legal contact with the chest or an arm bar.",
        focus: 52,
        ball: "coach",
        duration: 2600,
        positions: { coach: [80, 55], o1: [46, 39], d1: [53, 42] },
        movements: [
          { player: "o1", path: "curve-via", points: [{ position: [18, 24], offset: 0 }, { position: [34, 28], offset: 0.5 }, { position: [46, 39], offset: 1 }] },
          { player: "d1", path: "curve-via", points: [{ position: [50, 46], offset: 0 }, { position: [48, 38], offset: 0.55 }, { position: [53, 42], offset: 1 }] }
        ]
      },
      {
        title: "Deny and force the cutter out",
        description: "The defender denies the pass in the key and forces the cutter toward a less advantageous catch away from the basket.",
        focus: 58,
        ball: "coach",
        duration: 2600,
        positions: { coach: [80, 55], o1: [51, 73], d1: [58, 64] },
        movements: [
          { player: "o1", path: "curve-via", points: [{ position: [46, 39], offset: 0 }, { position: [43, 53], offset: 0.45 }, { position: [51, 73], offset: 1 }] },
          { player: "d1", path: "curve-via", points: [{ position: [53, 42], offset: 0 }, { position: [50, 53], offset: 0.45 }, { position: [58, 64], offset: 1 }] }
        ]
      },
      {
        title: "Play live on the catch",
        description: "If the cutter receives the pass, play one-on-one to the basket. The offensive player is limited to two dribbles.",
        focus: 43,
        ball: "o1",
        ballPosition: [50, 24],
        duration: 3000,
        positions: { coach: [80, 55], o1: [50, 24], d1: [56, 28] },
        ballPath: [
          { position: [80, 55], offset: 0, layer: "over" },
          { position: [51, 73], offset: 0.35, layer: "over" },
          { position: [58, 47], offset: 0.68, layer: "over" },
          { position: [50, 24], offset: 1, layer: "over" }
        ],
        movements: [
          { player: "o1", path: "curve-via", points: [{ position: [51, 73], offset: 0 }, { position: [51, 73], offset: 0.35 }, { position: [58, 47], offset: 0.68 }, { position: [50, 24], offset: 1 }] },
          { player: "d1", path: "curve-via", points: [{ position: [58, 64], offset: 0 }, { position: [58, 64], offset: 0.35 }, { position: [61, 43], offset: 0.68 }, { position: [56, 28], offset: 1 }] }
        ]
      },
      {
        title: "Rotate offense to defense",
        description: "After the repetition, the offensive player becomes the defender and the defender becomes the next cutter.",
        focus: 50,
        ball: "coach",
        duration: 2200,
        teamChangeDelay: 2100,
        teams: { coach: "neutral", o1: "defense", d1: "offense" },
        positions: { coach: [80, 55], o1: [50, 46], d1: [18, 24] },
        movements: [
          { player: "o1", path: "curve-via", points: [{ position: [50, 24], offset: 0 }, { position: [50, 46], offset: 1 }] },
          { player: "d1", path: "curve-via", points: [{ position: [56, 28], offset: 0 }, { position: [35, 18], offset: 0.5 }, { position: [18, 24], offset: 1 }] }
        ]
      }
    ]
  };
}());
