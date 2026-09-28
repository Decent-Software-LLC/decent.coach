(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["five-corner-passing"] = {
    id: "five-corner-passing", title: "Five Corner Passing", titleLines: ["Five Corner", "Passing"], status: "ready",
    categories: ["Passing", "Communication"], summary: "Five lines pass next-but-one around a star, then follow each pass through traffic to the receiving line.",
    variations: ["Begin with one ball for newer players.", "Specify the type of pass.", "Reverse direction on the coach's call."],
    pointsOfEmphasis: ["Call a name and show ten fingers.", "Step toward the ball to receive it.", "Use strong passing form and crisp passes."],
    equipment: { players: 10, playersLabel: "All Players", basketballs: 2 },
    extraBallIds: ["second"],
    court: { type: "half", asset: "assets/courts/basketball-halfcourt.svg", aspectRatio: "1090.86 / 912.61", label: "Half court", startingEnd: "top" },
    players: [
      { id:"p1",label:"1a",team:"offense" },{ id:"p1b",label:"1b",team:"offense" },
      { id:"p2",label:"2a",team:"offense" },{ id:"p2b",label:"2b",team:"offense" },
      { id:"p3",label:"3a",team:"offense" },{ id:"p3b",label:"3b",team:"offense" },
      { id:"p4",label:"4a",team:"offense" },{ id:"p4b",label:"4b",team:"offense" },
      { id:"p5",label:"5a",team:"offense" },{ id:"p5b",label:"5b",team:"offense" }
    ],
    steps: [
      { title: "Form five lines", description: "Form five evenly spaced lines with two players at every point of the star. Players 1a and 2a begin with basketballs.", focus: 50, ball: "p1", callouts:{p1:"3b"}, loopingCallouts:["p1"], extraBalls:{second:{position:[76,42]}}, positions: { p1:[50,22],p1b:[50,13],p2:[76,42],p2b:[85,35],p3:[66,73],p3b:[75,82],p4:[34,73],p4b:[25,82],p5:[24,42],p5b:[15,35] }, movements: [] },
      { title: "Pass across the star", description: "Player 1a calls Player 3a's name and delivers a crisp pass across the star. Player 3a steps toward the ball with ten fingers shown.", focus: 62, ball: "p3", extraBalls:{second:{position:[76,42]}}, duration: 3200, positions: { p1:[83,88],p1b:[50,22],p2:[76,42],p2b:[85,35],p3:[66,73],p3b:[75,82],p4:[34,73],p4b:[25,82],p5:[24,42],p5b:[15,35] }, ballPath:[{position:[50,22],offset:0},{position:[66,73],offset:.38},{position:[66,73],offset:1}], movements: [{player:"p1",path:"curve-via",points:[{position:[50,22],offset:0},{position:[50,22],offset:.38},{position:[50,58],offset:.62},{position:[50,88],offset:.78},{position:[76,94],offset:.91},{position:[83,88],offset:1}]},{player:"p1b",path:"curve-via",points:[{position:[50,13],offset:0},{position:[50,13],offset:.38},{position:[50,22],offset:1}]}] },
      { title: "Follow to the far side", description: "The passer runs to the far side of the receiving line, creating traffic for the next pass while the line advances.", focus: 50, ball: "p3", callouts:{p2:"4a"}, extraBalls:{second:{position:[34,73],path:[{position:[76,42],offset:0},{position:[76,42],offset:.4},{position:[34,73],offset:.58},{position:[34,73],offset:1}]}}, duration: 3400, positions: { p1:[83,88],p1b:[50,22],p2:[17,88],p2b:[76,42],p3:[66,73],p3b:[75,82],p4:[34,73],p4b:[25,82],p5:[24,42],p5b:[15,35] }, movements: [{player:"p2",path:"curve-via",points:[{position:[76,42],offset:0},{position:[76,42],offset:.58},{position:[19,61],offset:.76},{position:[10,80],offset:.9},{position:[17,88],offset:1}]},{player:"p2b",path:"curve-via",points:[{position:[85,35],offset:0},{position:[85,35],offset:.58},{position:[76,42],offset:1}]}] },
      { title: "Continue the star", description: "Player 3a passes next-but-one to Player 5a, then follows through the middle to the far side of that line.", focus: 42, ball: "p5", callouts:{p3:"5a"}, extraBalls:{second:{position:[34,73]}}, duration: 3400, positions: { p1:[83,88],p1b:[50,22],p2:[17,88],p2b:[76,42],p3:[8,29],p3b:[75,82],p4:[34,73],p4b:[25,82],p5:[24,42],p5b:[15,35] }, ballPath:[{position:[66,73],offset:0},{position:[66,73],offset:.4},{position:[24,42],offset:.58},{position:[24,42],offset:1}], movements: [{player:"p3",path:"curve-via",points:[{position:[66,73],offset:0},{position:[66,73],offset:.58},{position:[13,51],offset:.76},{position:[5,38],offset:.9},{position:[8,29],offset:1}]}] },
      { title: "Keep the rhythm", description: "Continue around the five-point pattern with both basketballs. Communicate early, meet every pass, and keep every line moving at game speed.", focus: 50, ball: "p5", callouts:{p4:"1b"}, extraBalls:{second:{position:[50,22],path:[{position:[34,73],offset:0},{position:[34,73],offset:.4},{position:[50,22],offset:.58},{position:[50,22],offset:1}]}}, duration: 3400, positions: { p1:[83,88],p1b:[50,22],p2:[17,88],p2b:[76,42],p3:[8,29],p3b:[75,82],p4:[50,6],p4b:[25,82],p5:[24,42],p5b:[15,35] }, movements: [{player:"p4",path:"curve-via",points:[{position:[34,73],offset:0},{position:[34,73],offset:.58},{position:[39,31],offset:.76},{position:[41,12],offset:.9},{position:[50,6],offset:1}]}] }
    ]
  };
}());
