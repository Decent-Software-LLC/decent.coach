(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["full-court-four-line-passing"] = {
    id: "full-court-four-line-passing", title: "Full Court Four Line Passing", titleLines: ["Full Court", "Four Line Passing"], status: "ready",
    categories: ["Passing", "Transition"], summary: "Four lanes advance at full speed while crossing passes create traffic before an outside player cuts for a lay-up.",
    variations: ["Pass to the adjacent line for younger players.", "Have outside lines exchange long passes while inside lines exchange shorter passes."],
    pointsOfEmphasis: ["Run at full speed instead of stopping to pass.", "Lead moving receivers.", "Show ten fingers and call a name."],
    equipment: { players: 4, playersLabel: "All Players", basketballs: 2 },
    court: { type:"full", asset:"assets/courts/basketball-fullcourt.svg", aspectRatio:"5 / 3", label:"Full court", startingEnd:"left", overlay:{asset:"assets/basketball-hoop.png",alt:"Far basket",left:84.8,top:45,width:10,rotation:90} },
    players: [1,2,3,4].map(n => ({ id:`p${n}`, label:String(n), team:"offense" })),
    steps: [
      { title:"Start in four lanes", description:"Form four lines across the baseline. Players 1 and 2 begin with basketballs while all four runners face up court.", focus:5, ball:"p1", positions:{p1:[5,22],p2:[5,40],p3:[5,60],p4:[5,78]}, movements:[] },
      { title:"Pass across the traffic", description:"All four players run in their lanes. Player 1 passes across to Player 3 and receives the return while Player 2 exchanges with Player 4.", focus:34, ball:"p3", ballArrival:.42, duration:3000, positions:{p1:[34,22],p2:[34,40],p3:[34,60],p4:[34,78]}, movements:[] },
      { title:"Advance without stopping", description:"Keep sprinting and exchange another pass across the lanes, leading the receiver and maintaining spacing through midcourt.", focus:61, ball:"p2", ballArrival:.45, duration:3000, positions:{p1:[61,22],p2:[61,40],p3:[61,60],p4:[61,78]}, movements:[] },
      { title:"Cut for the lay-up", description:"At the far free-throw line extended, the outside player cuts hard to the basket and receives a pass in stride for the lay-up.", focus:88, ball:"p1", duration:3600, positions:{p1:[89,50],p2:[78,45],p3:[82,60],p4:[83,78]}, ballPath:[{position:[61,40],offset:0},{position:[78,45],offset:.4},{position:[86,39],offset:.56},{position:[86,39],offset:.62},{position:[89,50],offset:1}], movements:[{player:"p1",path:"curve-via",points:[{position:[61,22],offset:0},{position:[78,27],offset:.4},{position:[86,39],offset:.56},{position:[86,39],offset:.62},{position:[89,50],offset:1}]},{player:"p2",path:"curve-via",points:[{position:[61,40],offset:0},{position:[78,45],offset:.4},{position:[78,45],offset:1}]}] },
      { title:"Exchange lines and return", description:"Inside and outside players exchange lines, then return down court using the same full-speed passing pattern.", focus:72, ball:"p3", ballArrival:.45, duration:3000, positions:{p1:[86,60],p2:[86,78],p3:[86,22],p4:[86,40]}, movements:[] }
    ]
  };
}());
