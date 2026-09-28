(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["mirror-drills"] = {
    id: "mirror-drills",
    title: "Mirror Drills",
    titleLines: ["Mirror", "Drills"],
    status: "ready",
    categories: ["Defense", "Footwork"],
    summary: "Defenders mirror a leader's lateral movement while maintaining proper stance, spacing, and quick changes of direction.",
    variations: [
      "Use the coach-led formation with players staying aligned behind the coach.",
      "Pair players along a court line with one leader and one mirror."
    ],
    pointsOfEmphasis: [
      "Maintain a correct defensive stance: start wide, then get wider.",
      "Use quick lateral footwork without crossing the feet.",
      "Limit the leader to three steps before changing direction.",
      "Switch leader and follower after 30 seconds."
    ],
    equipment: { players: 5, basketballs: 0 },
    court: {
      type: "half",
      asset: "assets/courts/basketball-halfcourt.svg",
      aspectRatio: "1090.86 / 912.61",
      label: "Half court",
      startingEnd: "top"
    },
    players: [
      { id: "d1", label: "1", team: "defense" },
      { id: "d2", label: "2", team: "defense" },
      { id: "d3", label: "3", team: "defense" },
      { id: "d4", label: "4", team: "defense" },
      { id: "d5", label: "5", team: "defense" },
      { id: "coach", label: "C", team: "neutral" }
    ],
    steps: [
      {
        title: "Set a defensive stance",
        description: "Players form a straight line facing the coach. Begin low and balanced with the feet wide, chest up, and hands active.",
        focus: 50,
        ball: null,
        positions: { d1: [50, 28], d2: [50, 38], d3: [50, 48], d4: [50, 58], d5: [50, 68], coach: [50, 82] },
        movements: []
      },
      {
        title: "Mirror the coach",
        description: "The coach moves laterally and every defender slides with the coach while staying in line and maintaining proper defensive spacing.",
        focus: 38,
        ball: null,
        duration: 1900,
        positions: { d1: [31, 28], d2: [31, 38], d3: [31, 48], d4: [31, 58], d5: [31, 68], coach: [31, 82] },
        movements: []
      },
      {
        title: "Change direction quickly",
        description: "After no more than three steps, the coach changes direction. Players push off the outside foot and stay square without crossing their feet.",
        focus: 58,
        ball: null,
        duration: 2300,
        positions: { d1: [69, 28], d2: [69, 38], d3: [69, 48], d4: [69, 58], d5: [69, 68], coach: [69, 82] },
        movements: []
      },
      {
        title: "Work in pairs",
        description: "Pair up along a court line. One partner leads with short lateral movements while the defender stays directly in front like a mirror.",
        focus: 50,
        ball: null,
        duration: 2400,
        positions: { d1: [28, 43], d2: [28, 61], d3: [50, 43], d4: [50, 61], d5: [72, 43], coach: [72, 61] },
        movements: []
      },
      {
        title: "Switch leader and follower",
        description: "After 30 seconds, partners exchange roles and repeat the drill with the same quickness, stance, and disciplined footwork.",
        focus: 50,
        ball: null,
        duration: 1800,
        positions: { d1: [28, 61], d2: [28, 43], d3: [50, 61], d4: [50, 43], d5: [72, 61], coach: [72, 43] },
        movements: []
      }
    ]
  };
}());
