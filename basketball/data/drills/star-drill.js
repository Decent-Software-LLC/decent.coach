(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["star-drill"] = {
    id:"star-drill", title:"Star Drill", titleLines:["Star Drill"], status:"ready", localOnly:true,
    categories:["Passing","Lay-ups","Receiving"], summary:"Five positions move the ball around the lane in a star sequence before the final receiver attacks for a lay-up.",
    variations:["Add a second ball after the first reaches Position 4.","Reverse direction for left-hand lay-ups.","Specify the pass or finishing type.","Finish with a short pull-up instead of a lay-up."],
    pointsOfEmphasis:["Make every pass hard and accurate.","Call the passer's name and show ten fingers.","Step toward every pass.","Drive hard and finish with correct lay-up form."],
    equipment:{players:6,playersLabel:"All Players",basketballs:1},
    court:{type:"half",asset:"assets/courts/basketball-halfcourt.svg",aspectRatio:"1090.86 / 912.61",label:"Half court",startingEnd:"top",overlay:{asset:"assets/basketball-hoop.png",alt:"Aerial basketball hoop and backboard",left:43,top:12,width:14}},
    players:[1,2,3,4,5,6].map(n=>({id:`p${n}`,label:String(n),team:"offense"})),
    steps:[
      {title:"Set the five-point star",description:"Place Players 3 and 4 near the low lane spaces, Players 2 and 5 near the elbows, and the remaining players in a baseline line. Player 1 starts with the ball.",focus:40,ball:"p1",positions:{p1:[50,82],p2:[34,48],p3:[37,30],p4:[63,30],p5:[66,48],p6:[50,92]},movements:[]},
      {title:"Pass and follow to Position 2",description:"Player 1 passes to Player 2, calls the name, and follows the pass to replace Player 2.",focus:47,ball:"p2",ballArrival:.45,duration:2600,positions:{p1:[34,48],p2:[37,30],p3:[50,40],p4:[63,30],p5:[66,48],p6:[50,82]},movements:[{player:"p1",path:"curve-via",points:[{position:[50,82],offset:0},{position:[50,82],offset:.45},{position:[34,48],offset:1}]}]},
      {title:"Move through the low positions",description:"Player 2 passes to Player 3 and follows. Player 3 then passes across to Player 4 and replaces that position.",focus:38,ball:"p4",duration:3200,positions:{p1:[34,48],p2:[37,30],p3:[63,30],p4:[66,48],p5:[58,40],p6:[50,82]},ballPath:[{position:[37,30],offset:0},{position:[50,40],offset:.35},{position:[50,40],offset:.45},{position:[63,30],offset:.72},{position:[66,48],offset:1}],movements:[{player:"p2",path:"curve-via",points:[{position:[37,30],offset:0},{position:[50,40],offset:.45},{position:[37,30],offset:1}]},{player:"p3",path:"curve-via",points:[{position:[50,40],offset:0},{position:[50,40],offset:.45},{position:[63,30],offset:1}]}]},
      {title:"Deliver to the final receiver",description:"Player 4 passes to Player 5 and follows the pass. Player 5 catches ready to drive hard toward the basket.",focus:43,ball:"p5",ballArrival:.5,duration:2600,positions:{p1:[34,48],p2:[37,30],p3:[63,30],p4:[66,48],p5:[60,38],p6:[50,82]},movements:[]},
      {title:"Drive and finish",description:"Player 5 attacks with one strong dribble and finishes the lay-up. The shooter rebounds and returns the ball to the next player in line.",focus:24,ball:"p5",duration:3200,positions:{p1:[34,48],p2:[37,30],p3:[63,30],p4:[66,48],p5:[50,20],p6:[50,82]},movements:[{player:"p5",path:"curve-via",points:[{position:[60,38],offset:0},{position:[55,29],offset:.5},{position:[50,20],offset:1}]}]},
      {title:"Continue the rotation",description:"Each passer follows to the next position. The finisher rebounds, hands the ball to the baseline line, and joins the end of that line.",focus:50,ball:"p6",ballArrival:.5,duration:2800,positions:{p1:[37,30],p2:[63,30],p3:[66,48],p4:[60,38],p5:[50,92],p6:[50,82]},movements:[]}
    ]
  };
}());
