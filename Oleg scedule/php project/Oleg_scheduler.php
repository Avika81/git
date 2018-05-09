<?php

require_once __DIR__ . '/Simplex-Calculator-master/Simplex/simplex.php';
require_once __DIR__ . '/lp_solve_5.5_PHP/extra/PHP/lp_solve.php';
echo "start\n";

$debug = True;
$epsilon = 0.01;
$max_shift_time = 12.0;
$days = array("Sun","Mon","Tue","Wed","Thu","Fri","Sat");
$number_of_days = sizeof($days);
$one = 1;
$zero = 0;
$minus_one = -1;

class Time{
  function Time($day,$start,$end){
    $this->day = $day;
    $this->start = $start;
    $this->end = $end;
  }
}

class Employee{
  function Employee($id,$name,$availability, $jobs, $max_day = array(4,4,4,4,4,4,4), $max_week = 20){
    $this->id = $id;
    $this->name = $name;
    $this->availability = $availability;
    $this->jobs = $jobs;
    $this->max_day = $max_day;
    $this->max_week = $max_week;
  }
}

class Shift{
  function Shift($id,$time,$job_id,$number_employees_needed = 1){
    $this->id = $id;
    $this->time = $time;
    $this->job_id = $job_id;
    $this->number_employees_needed = $number_employees_needed;
  }
}


$employees =array(new Employee(1,"Employee1",array(
    new Time("Sun",0,24),
    new Time("Mon",0,24),
    new Time("Tue",0,24),
    new Time("Wed",0,24),
    new Time("Thu",0,24),
    new Time("Fri",0,24),
    new Time("Sat",0,24)
    ),
  array(1,2,3,4)
  )
);

$shifts = array(
  new Shift(0,new Time("Sun",8,10),1),
  new Shift(1,new Time("Sun",8,10),1),
  new Shift(2,new Time("Sun",11,13),1),
  new Shift(3,new Time("Sun",8,10),1)
);

$number_of_employees = sizeof($employees);
$number_of_shifts = sizeof($shifts);

function collision($x,$y){
  if($x->day != $y->day){
    return False;
  }
  if($x->end < $y->start){
    return False;
  }
  if($x->start > $y->end){
    return False;
  }
  return True;
}

function in_time($x,$y){
  if($x->day!=$y->day){
    return False;
  }
  if($x->start<$y->start){
    return False;
  }
  if($x->end>$y->end){
    return False;
  }
  return True;
}

function could_do_this_job($s,$e){
  $has_this_job_id = False;
  foreach($e->jobs as $j){
    if($j == $s->job_id){
      $has_this_job_id = True;
    }
  }
  if(!$has_this_job_id){
    return False;
  }
  foreach($e->availability as $t){
    if(in_time($s->time,$t)){
      return True;
    }
  }
  return False;
}

function total_time($t){
  $res = $t->end - $t->start;
  return $res;
}

function get_index($employee,$shift,$number_of_shifts){
  return($employee*$number_of_shifts+$shift);
}

function zeros($number_of_variables){
  $output = array_fill(0,(int)$number_of_variables,0);
  return $output;
}

function print_matrix($A,$b,$eq){
  for($row = 0;$row<sizeof($A);$row++){
    $Astr = implode(",",$A[$row]);
    echo $Astr;
    switch($eq[$row]){
      case -1:echo "<=";break;
      case 0:echo "=";break;
      case 1:echo ">=";break;
    }
    echo $b[$row];
    echo "\n";

  }
}


$number_of_variables = $number_of_shifts * $number_of_employees;

$A = array();
$b = array();
$c = array();
$eq = array();

#each employee is able to work in a single shift only one time
for($i = 0;$i<$number_of_variables;$i++){
  $new_line = zeros($number_of_variables);
  $new_line[$i] = 1;
  array_push($A,$new_line);
  array_push($b,$one);
  array_push($eq,$minus_one); //Less than
}

#shifts constraints:
for($s = 0; $s < $number_of_shifts; $s++){
  $new_line = zeros($number_of_variables);
  for($e = 0;$e<$number_of_employees;$e++){
    if(could_do_this_job($shifts[$s], $employees[$e])){
      $new_line[get_index($e,$s,$number_of_shifts)] = 1;
    }
    else {
      $nl = zeros($number_of_variables);
      $nl[get_index($e,$s,$number_of_shifts)] =1;
      array_push($A,$nl);
      array_push($b,$zero);
      array_push($eq,$zero); //equality constraint
    }
  }
}

#week constraints:
for($e = 0;$e<$number_of_employees;$e++){
  $new_line = zeros($number_of_variables);
  for($s = 0;$s<$number_of_shifts;$s++){
    $new_line[get_index($e,$s,$number_of_shifts)] = total_time($shifts[$s]->time);  # the length of this shift
  }
  array_push($A,$new_line);
  array_push($b,$employees[$e]->max_week);
  array_push($eq,$minus_one);
}


#day constraints:
for($e = 0; $e<$number_of_employees;$e++){
  for($d = 0;$d<$number_of_days;$d++){
    $new_line=zeros($number_of_variables);
    for($s = 0;$s<$number_of_shifts;$s++){
      if($shifts[$s]->time->day == $days[$d]){
        $new_line[get_index($e,$s,$number_of_shifts)] = 1;
      }
    }
    array_push($A,$new_line);
    array_push($b,$employees[$e]->max_day[$d]);
    array_push($eq,$minus_one);
  }
}

#check that each employee is only in one place at a time
for($s1=0;$s1<$number_of_shifts;$s1++){
  $l_collisions = array();
  for($s2=0;$s2<$number_of_shifts;$s2++){
    if($s1>=$s2){
      continue;
    }
    if(collision($shifts[$s1]->time,$shifts[$s2]->time)){
      array_push($l_collisions,$s2);
    }
  }
  for($e = 0;$e<$number_of_employees;$e++){
    $new_line = zeros($number_of_variables);
    $new_line[get_index($e,$s1,$number_of_shifts)] = 1;
    for($s2=0;$s2<$number_of_shifts;$s2++){
      $new_line[get_index($e,$s2,$number_of_shifts)] = 1;
    }
    array_push($A,$new_line);
    array_push($b,$one);
    array_push($eq,$minus_one);
  }
}

if($debug){
  print_matrix($A,$b,$eq);
}

$c = array();
for($i=0;$i<$number_of_variables;$i++){
  $bonus = rand(0,10);
  array_push($c,-1-$bonus);
}

$arr = lp_solve($c,$A,$b,$e);







// $z = new Simplex\Func(array(
// 	'x1' => 1,
// 	'x2' => 2,
// ));
// $task = new Simplex\Task($z);
// $task->addRestriction(new Simplex\Restriction(array(
// 	'x1' => 3,
// 	'x2' => 2,
// ), Simplex\Restriction::TYPE_LOE, 24));
// $task->addRestriction(new Simplex\Restriction(array(
// 	'x1' => -2,
// 	'x2' => -4,
// ), Simplex\Restriction::TYPE_GOE, -32));
// $solver = new Simplex\Solver($task);
//var_dump($solver);

?>
