(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["knockout"] = {
    id:"knockout",title:"Knockout",titleLines:["Knockout"],status:"ready",categories:["Shooting","Rebounding"],summary:"Two shooters race to score, rebound, and return the ball before the trailing shooter makes a basket.",
    variations:["Start the first shot from the wing or three-point line."],pointsOfEmphasis:["Use correct shooting form.","Do not follow the first shot until it reaches the rim.","Rebound strongly.","Avoid traveling after a missed shot."],
    equipment:{players:5,playersLabel:"All Players",basketballs:2},extraBallIds:["second"],
    court:{type:"half",asset:"assets/courts/basketball-halfcourt.svg",aspectRatio:"1090.86 / 912.61",label:"Half court",startingEnd:"top",overlay:{asset:"assets/basketball-hoop.png",alt:"Aerial basketball hoop and backboard",left:43,top:12,width:14}},
    players:[1,2,3,4,5].map(n=>({id:`p${n}`,label:String(n),team:"offense"})),
    steps:[
      {title:"Form one shooting line",description:"Line up at the free-throw line. Players 1 and 2 begin with basketballs, with Player 1 at the front.",focus:50,ball:"p1",extraBalls:{second:{position:[50,58]}},positions:{p1:[50,49],p2:[50,58],p3:[50,67],p4:[50,76],p5:[50,85]},movements:[]},
      {title:"First shooter releases",description:"Player 1 takes the first shot using correct form and waits until the ball reaches the rim before pursuing it.",focus:32,ball:"p1",ballPosition:[50,20],extraBalls:{second:{position:[50,58]}},duration:2600,positions:{p1:[50,41],p2:[50,58],p3:[50,67],p4:[50,76],p5:[50,85]},ballPath:[{position:[50,49],offset:0},{position:[50,12],offset:.72},{position:[50,20],offset:1}],movements:[]},
      {title:"Second shooter gives chase",description:"After Player 1 shoots, Player 2 takes the next shot. Player 1 rebounds and continues shooting after a miss while Player 2 tries to score first.",focus:30,ball:"p1",ballPosition:[43,28],extraBalls:{second:{position:[50,20],path:[{position:[50,58],offset:0},{position:[50,58],offset:.2},{position:[50,12],offset:.78},{position:[50,20],offset:1}]}},duration:3200,positions:{p1:[43,28],p2:[50,41],p3:[50,58],p4:[50,67],p5:[50,76]},movements:[{player:"p1",path:"curve-via",points:[{position:[50,41],offset:0},{position:[50,41],offset:.55},{position:[43,28],offset:1}]}]},
      {title:"Score, return, and rotate",description:"After scoring, the shooter rebounds, returns the ball to the next player, and joins the end of the line. A trailing shooter who scores first knocks out the player ahead.",focus:50,ball:"p3",extraBalls:{second:{position:[50,49]}},duration:3000,positions:{p1:[50,85],p2:[50,32],p3:[50,49],p4:[50,58],p5:[50,67]},movements:[{player:"p1",path:"curve-via",points:[{position:[43,28],offset:0},{position:[30,48],offset:.35},{position:[35,78],offset:.7},{position:[50,85],offset:1}]}]}
    ]
  };
}());
