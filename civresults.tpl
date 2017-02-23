<title> {{attackerlevel}} {{attacker}} vs. {{defenderlevel}} {{defender}} </title>


What happens when a {{attackerlevel}} {{attacker}} attacks a {{defenderlevel}} {{defender}} 
% if fortified==True:
fortified
% end

% if location=="walledcity":
in a walled city
% elif location=="city":
in an unwalled city
% elif location=="fort":
in a fort 
%elif location=="open":
out in the open 
% end

% if river=="True":
on a river
%end
on {{terrain}}:
<p>


The attacking {{attacker}} has strength {{attackervalue}}. 
{{attackerlevel}} multiplies it by {{attackerlevelmultiplier}} to get <b>{{attackerlevelvalue}}</b>.
<p>

The defending {{defender}} has strength {{defendervalue}}. {{defenderlevel}} multiplies it by {{defenderlevelmultiplier}} to get <b>{{defenderlevelvalue}}</b>.
<p>

The defending {{defender}} is on {{terrain}} which gives a x{{terrainmultiplier}} bonus, making the defence score {{terrainvalue}}.

