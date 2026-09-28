(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["pig-in-the-middle"] = {
    id:"pig-in-the-middle",title:"Pig In The Middle",titleLines:["Pig In","The Middle"],status:"ready",categories:["Passing","Defense"],summary:"Two passers protect the ball across a short gap while one defender pressures the ball and tries to earn a deflection.",
    variations:["Give each passer a three-second limit to release the ball."],pointsOfEmphasis:["Fake a pass to make a pass.","Step into or around the defender to create the passing lane.","The defender calls 'ball' and applies aggressive pressure."],
    equipment:{players:3,basketballs:1},court:{type:"half",asset:"assets/courts/basketball-halfcourt.svg",aspectRatio:"1090.86 / 912.61",label:"Half court",startingEnd:"top"},
    players:[{id:"o1",label:"1",team:"offense"},{id:"o2",label:"2",team:"offense"},{id:"d1",label:"X1",team:"defense"}],
    steps:[
      {title:"Set a three-player group",description:"Two passers stand several metres apart with one defender between them. Player 1 begins with the basketball.",focus:50,ball:"o1",positions:{o1:[30,55],o2:[70,55],d1:[50,55]},movements:[]},
      {title:"Pressure the ball",description:"The defender closes aggressively on Player 1 and calls 'ball.' Player 1 protects the basketball and uses a strong pass fake.",focus:40,duration:2400,ball:"o1",positions:{o1:[30,55],o2:[70,55],d1:[39,55]},movements:[]},
      {title:"Create and complete the pass",description:"Player 1 steps into or around the defender and passes to Player 2. The defender attacks the passing lane, then recovers to pressure the new ball-handler.",focus:58,ball:"o2",ballArrival:.55,duration:2800,positions:{o1:[27,52],o2:[70,55],d1:[59,55]},movements:[{player:"d1",path:"curve-via",points:[{position:[39,55],offset:0},{position:[50,49],offset:.45},{position:[59,55],offset:1}]}]},
      {title:"Deflect and exchange roles",description:"When the defender touches or intercepts a pass, the defender exchanges places with the passer who released it and the drill immediately continues.",focus:50,ball:"d1",ballPosition:[49,54],duration:3000,teamChangeDelay:2600,teams:{o1:"defense",o2:"offense",d1:"offense"},positions:{o1:[50,55],o2:[70,55],d1:[30,55]},ballPath:[{position:[70,55],offset:0},{position:[49,54],offset:.45},{position:[30,55],offset:1}],movements:[{player:"o1",path:"curve-via",points:[{position:[27,52],offset:0},{position:[40,48],offset:.5},{position:[50,55],offset:1}]},{player:"d1",path:"curve-via",points:[{position:[59,55],offset:0},{position:[49,54],offset:.45},{position:[30,55],offset:1}]}]}
    ]
  };
}());
