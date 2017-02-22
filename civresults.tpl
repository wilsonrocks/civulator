When a {{attackerlevel}} {{attacker}} attacks a {{defenderlevel}} {{defender}} 
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
on {{terrain}}.
<p>


{{attacker}} has strength {{attackervalue}}. 
{{attackerlevel}} multiplies it by {{attackerlevelmultiplier}} to get <b>{{attackerlevelvalue}}</b>.

