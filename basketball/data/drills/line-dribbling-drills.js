(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["line-dribbling-drills"] = {
    id:"line-dribbling-drills", title:"Line Dribbling Drills", titleLines:["Line Dribbling", "Drills"], status:"ready",
    categories:["Dribbling","Ball Handling"], summary:"Players advance in lanes and execute controlled changes of speed, direction, and hand at designated court marks.",
    variations:["Use follow-the-leader, with every player copying the designated leader's moves."],
    pointsOfEmphasis:["Keep the head up and use fingertips, not palms.","Protect the ball and stay low and balanced.","Plant and push off explosively when changing direction."],
    equipment:{players:4,playersLabel:"All Players",basketballs:4},
    playerBalls:["p1","p2","p3","p4"],
    court:{type:"full",asset:"assets/courts/basketball-fullcourt.svg",aspectRatio:"5 / 3",label:"Full court",startingEnd:"left"},
    players:[1,2,3,4].map(n=>({id:`p${n}`,label:String(n),team:"offense"})),
    steps:[
      {title:"Set four dribbling lanes",description:"Form four lines on the baseline. Each player begins low and balanced with a basketball and eyes up.",focus:5,ball:"p1",positions:{p1:[5,20],p2:[5,40],p3:[5,60],p4:[5,80]},movements:[]},
      {title:"Change pace under control",description:"Advance with a speed dribble, then lower the body and shift into a protected control dribble at the designated mark.",focus:30,ball:"p1",duration:2800,positions:{p1:[30,20],p2:[30,40],p3:[30,60],p4:[30,80]},movements:[]},
      {title:"Execute the designated move",description:"At the next mark, use the coach's selected move: crossover, inside-out, reverse, or hesitation. Stay low and protect the ball.",focus:53,ball:"p1",duration:3000,positions:{p1:[53,27],p2:[53,34],p3:[53,67],p4:[53,73]},movements:[{player:"p1",path:"curve-via",points:[{position:[30,20],offset:0},{position:[40,20],offset:.4},{position:[46,28],offset:.65},{position:[53,27],offset:1}]},{player:"p4",path:"curve-via",points:[{position:[30,80],offset:0},{position:[40,80],offset:.4},{position:[46,72],offset:.65},{position:[53,73],offset:1}]}]},
      {title:"Attack out of the move",description:"Plant the outside foot, push off explosively, and accelerate into open court without losing balance or looking down.",focus:78,ball:"p1",duration:2800,positions:{p1:[78,27],p2:[78,34],p3:[78,67],p4:[78,73]},movements:[]},
      {title:"Finish and change direction",description:"Finish at the far end under control. On the next repetition, use a zig-zag route with crossover, behind-the-back, or between-the-legs changes.",focus:91,ball:"p1",duration:2600,positions:{p1:[91,35],p2:[91,44],p3:[91,56],p4:[91,65]},movements:[]}
    ]
  };
}());
