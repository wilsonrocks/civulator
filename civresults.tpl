<title> {{attackerlevel}} {{attacker}} vs. {{defenderlevel}} {{defender}} </title>


The story of what happens when a {{attackerlevel}} {{attacker}} attacks a {{defenderlevel}} {{defender}}

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

Attacking {{attacker}}:<p>
Combat strength = {{attackervalue}}<p>
{{attackerlevel}} multiplier of {{attackerlevelmultiplier}} &#x21D2 {{attackerlevelvalue}}<p>

<p>
Defending {{defender}}:<p>
Combat Strength = {{defendervalue}}<p>
{{defenderlevel}} multiplier of {{defenderlevelmultiplier}} &#x21D2 {{defenderlevelvalue}}<p>

{{terrain}} multiplier of {{terrainmultiplier}} &#x21D2 {{terrainvalue}}<p>
