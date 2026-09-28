(function () {
  window.BASKETBALL_DRILLS = window.BASKETBALL_DRILLS || {};
  window.BASKETBALL_DRILLS["pass-shoot-and-rebound"] = {
    id:"pass-shoot-and-rebound", title:"Pass, Shoot And Rebound", titleLines:["Pass, Shoot", "And Rebound"], status:"ready",
    categories:["Shooting","Passing","Rebounding"], summary:"A three-player shooting sequence connects the rebounder, passer, and shooter before repeating or rotating roles.",
    variations:["Run for a set time, then rotate roles.","Rotate after every shot.","Require a dribble, relocation, shot fake, or jab step before the shot."],
    pointsOfEmphasis:["Use correct shooting form.","Chin and protect the rebound, then pivot away to pass.","Receive low and ready; pass into the shooting pocket."],
    equipment:{players:3,basketballs:1},
    court:{type:"half",asset:"assets/courts/basketball-halfcourt.svg",aspectRatio:"1090.86 / 912.61",label:"Half court",startingEnd:"top",overlay:{asset:"assets/basketball-hoop.png",alt:"Aerial basketball hoop and backboard",left:43,top:12,width:14}},
    players:[{id:"r",label:"R",team:"offense"},{id:"p",label:"P",team:"offense"},{id:"s",label:"S",team:"offense"}],
    steps:[
      {title:"Assign three roles",description:"Set one rebounder under the basket, one passer on the wing, and one shooter in shooting range. The rebounder starts with the ball.",focus:42,ball:"r",positions:{r:[50,27],p:[76,55],s:[24,55]},movements:[]},
      {title:"Outlet to the passer",description:"The rebounder protects the ball, pivots away from pressure, and delivers a strong pass to the passer in a ready stance.",focus:58,ball:"p",ballArrival:.55,duration:2400,positions:{r:[50,27],p:[76,55],s:[24,55]},movements:[]},
      {title:"Hit the shooting pocket",description:"The passer quickly moves the ball to the shooter's pocket. The shooter receives low, balanced, and ready to score.",focus:48,ball:"s",ballArrival:.55,duration:2400,positions:{r:[50,27],p:[76,55],s:[30,48]},movements:[]},
      {title:"Shoot and rebound",description:"The shooter uses correct form and releases the shot. The rebounder tracks the flight, secures the rebound, and protects it with two hands.",focus:25,ball:"r",duration:3200,positions:{r:[50,25],p:[76,55],s:[34,38]},ballPath:[{position:[30,48],offset:0},{position:[45,15],offset:.5},{position:[50,18],offset:.65},{position:[50,25],offset:1}],movements:[{player:"r",path:"curve-via",points:[{position:[50,27],offset:0},{position:[55,31],offset:.45},{position:[50,25],offset:1}]}]},
      {title:"Repeat or rotate",description:"Repeat for the assigned time or rotate roles after the shot so every player practices passing, shooting, and rebounding.",focus:48,ball:"r",duration:2200,positions:{r:[24,55],p:[50,27],s:[76,55]},movements:[]}
    ]
  };
}());
