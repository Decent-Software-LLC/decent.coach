(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["five-on-four-plus-one"] = {
    id: "five-on-four-plus-one",
    title: "Five On Four Plus One",
    titleLines: ["Five On Four", "Plus One"],
    status: "ready",
    categories: ["Transition", "Defense", "Advantage"],
    summary: "Five attackers push against four retreating defenders while a delayed fifth defender sprints back into the play.",
    variations: [],
    pointsOfEmphasis: [
      "Defenders must sprint back and get behind the ball.",
      "Protect the basket first.",
      "A defender must stop the ball-handler.",
      "Communicate continuously through the transition."
    ],
    equipment: { players: 10, playersLabel: "10 Players + Coach", basketballs: 1 },
    court: {
      type: "full",
      asset: "assets/courts/basketball-fullcourt.svg",
      aspectRatio: "5 / 3",
      label: "Full court",
      startingEnd: "left",
      overlay: {
        asset: "assets/basketball-hoop.png",
        alt: "Aerial basketball hoop and backboard at the far basket",
        left: 84.8,
        top: 45,
        width: 10,
        rotation: 90
      }
    },
    players: [
      { id: "coach", label: "C", team: "neutral" },
      { id: "o1", label: "1", team: "offense" },
      { id: "o2", label: "2", team: "offense" },
      { id: "o3", label: "3", team: "offense" },
      { id: "o4", label: "4", team: "offense" },
      { id: "o5", label: "5", team: "offense" },
      { id: "d1", label: "X1", team: "defense" },
      { id: "d2", label: "X2", team: "defense" },
      { id: "d3", label: "X3", team: "defense" },
      { id: "d4", label: "X4", team: "defense" },
      { id: "d5", label: "X5", team: "defense" }
    ],
    steps: [
      {
        title: "Set the transition teams",
        description: "Five offensive players line up across the baseline. Their defenders begin across the free-throw line extended while the coach holds the ball.",
        focus: 10,
        ball: "coach",
        positions: { coach: [14, 80], o1: [5, 16], o2: [5, 33], o3: [5, 50], o4: [5, 67], o5: [5, 84], d1: [20, 16], d2: [20, 33], d3: [20, 50], d4: [20, 67], d5: [20, 84] },
        movements: []
      },
      {
        title: "Pass and release",
        description: "The coach passes to an offensive player, and all five attackers immediately fill the lanes and push into transition.",
        focus: 29,
        ball: "o3",
        duration: 3000,
        positions: { coach: [14, 80], o1: [30, 16], o2: [30, 33], o3: [30, 50], o4: [30, 67], o5: [30, 84], d1: [35, 20], d2: [5, 24], d3: [35, 40], d4: [35, 60], d5: [35, 80] },
        ballPath: [
          { position: [14, 80], offset: 0, layer: "over" },
          { position: [5, 33], offset: 0.14, layer: "over" },
          { position: [5, 33], offset: 0.24, layer: "over" },
          { position: [16, 33], offset: 0.5, layer: "over" },
          { position: [5, 50], offset: 0.58, layer: "over" },
          { position: [5, 50], offset: 0.62, layer: "over" },
          { position: [30, 50], offset: 1, layer: "over" }
        ],
        movements: [
          { player: "o1", path: "curve-via", points: [{ position: [5, 16], offset: 0 }, { position: [5, 16], offset: 0.24 }, { position: [30, 16], offset: 1 }] },
          { player: "o2", path: "curve-via", points: [{ position: [5, 33], offset: 0 }, { position: [5, 33], offset: 0.24 }, { position: [16, 33], offset: 0.5 }, { position: [30, 33], offset: 1 }] },
          { player: "o3", path: "curve-via", points: [{ position: [5, 50], offset: 0 }, { position: [5, 50], offset: 0.62 }, { position: [30, 50], offset: 1 }] },
          { player: "o4", path: "curve-via", points: [{ position: [5, 67], offset: 0 }, { position: [5, 67], offset: 0.24 }, { position: [30, 67], offset: 1 }] },
          { player: "o5", path: "curve-via", points: [{ position: [5, 84], offset: 0 }, { position: [5, 84], offset: 0.24 }, { position: [30, 84], offset: 1 }] },
          { player: "d2", path: "curve-via", points: [{ position: [20, 33], offset: 0 }, { position: [17, 24], offset: 0.14 }, { position: [5, 24], offset: 0.38 }, { position: [5, 24], offset: 1 }] }
        ]
      },
      {
        title: "Protect the basket four-on-five",
        description: "Four defenders sprint back, protect the basket, stop the ball, and communicate matchups while the offense attacks its temporary advantage.",
        focus: 64,
        ball: "o3",
        duration: 3400,
        positions: { coach: [14, 80], o1: [82, 28], o2: [66, 34], o3: [68, 50], o4: [66, 66], o5: [82, 72], d1: [87, 36], d2: [45, 33], d3: [77, 43], d4: [77, 57], d5: [87, 64] },
        movements: [
          { player: "o1", path: "curve-via", points: [{ position: [30, 16], offset: 0 }, { position: [58, 18], offset: 0.32 }, { position: [82, 28], offset: 0.68 }, { position: [82, 28], offset: 1 }] },
          { player: "o5", path: "curve-via", points: [{ position: [30, 84], offset: 0 }, { position: [58, 82], offset: 0.32 }, { position: [82, 72], offset: 0.68 }, { position: [82, 72], offset: 1 }] },
          { player: "d1", path: "curve-via", points: [{ position: [35, 20], offset: 0 }, { position: [62, 25], offset: 0.32 }, { position: [87, 36], offset: 0.68 }, { position: [87, 36], offset: 1 }] },
          { player: "d5", path: "curve-via", points: [{ position: [35, 80], offset: 0 }, { position: [62, 75], offset: 0.32 }, { position: [87, 64], offset: 0.68 }, { position: [87, 64], offset: 1 }] },
          { player: "d2", path: "curve-via", points: [{ position: [5, 24], offset: 0 }, { position: [22, 28], offset: 0.35 }, { position: [45, 33], offset: 1 }] }
        ]
      },
      {
        title: "Sprint the plus one into the play",
        description: "The delayed defender sprints behind the ball and rejoins the defense. The unit communicates, matches up, and completes the transition stop.",
        focus: 86,
        ball: "o3",
        duration: 3600,
        callouts: { d1: "1", d2: "2", d3: "3", d4: "4", d5: "5" },
        positions: { coach: [14, 80], o1: [82, 28], o2: [66, 34], o3: [68, 50], o4: [66, 66], o5: [82, 72], d1: [87, 36], d2: [72, 38], d3: [73, 50], d4: [72, 63], d5: [87, 64] },
        movements: [
          { player: "d2", path: "curve-via", points: [{ position: [45, 33], offset: 0 }, { position: [58, 43], offset: 0.4 }, { position: [66, 44], offset: 0.68 }, { position: [72, 38], offset: 1 }] }
        ]
      }
    ]
  };
}());
