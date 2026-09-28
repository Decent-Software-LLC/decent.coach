(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["line-running-drills"] = {
    id:"line-running-drills",title:"Line Running Drills",titleLines:["Line Running","Drills"],status:"ready",categories:["Footwork","Movement"],summary:"Four lines cross the court using a selected running style, then execute controlled stops, pivots, and changes of direction.",
    variations:["Use follow-the-leader with one player choosing each movement."],pointsOfEmphasis:["Use precise footwork.","Stay balanced and low.","Plant the outside foot and push off explosively when changing direction."],
    equipment:{players:4,playersLabel:"All Players",basketballs:0},court:{type:"full",asset:"assets/courts/basketball-fullcourt.svg",aspectRatio:"5 / 3",label:"Full court",startingEnd:"left"},
    players:[1,2,3,4].map(n=>({id:`p${n}`,label:String(n),team:"offense"})),
    steps:[
      {title:"Form four baseline lines",description:"Players form four evenly spaced lines on the baseline. The coach selects the running style and the stop or pivot to perform.",focus:12,positions:{p1:[7,25],p2:[7,42],p3:[7,58],p4:[7,75]},movements:[]},
      {title:"Run with controlled technique",description:"The first player in each line moves together using the designated style: normal jog, high heels, high knees, or grapevine.",focus:34,duration:2600,positions:{p1:[34,25],p2:[34,42],p3:[34,58],p4:[34,75]},movements:[]},
      {title:"Stop and pivot on command",description:"At the designated line or whistle, players execute the selected jump stop, stride stop, forward pivot, reverse pivot, or hesitation step.",focus:52,duration:2200,positions:{p1:[52,25],p2:[52,42],p3:[52,58],p4:[52,75]},movements:[]},
      {title:"Finish through the court",description:"Players regain balance, push off, and finish through the far baseline while maintaining spacing between all four lines.",focus:86,duration:3000,positions:{p1:[91,25],p2:[91,42],p3:[91,58],p4:[91,75]},movements:[]}
    ]
  };
}());
