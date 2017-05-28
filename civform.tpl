<html>
<body>

<form action="/combat" method="post">

Choose your attacker:

<select name="attackerlevel">
    % for level in veteranlevels:
        <option value="{{level}}">{{level}}</option>
    % end
</select>


<select name="attacker">
    % for unit in unitlist:
        <option value="{{unit}}">{{unit}}</option>
    % end
</select>



<p>

Choose your defender:

<select name="defenderlevel">
    % for level in veteranlevels:
        <option value="{{level}}">{{level}}</option>
    % end
</select>

<select name="defender">

    % for unit in unitlist:
        <option value="{{unit}}">{{unit}}</option>
    % end
</select>
<p>
On:
<select name="terrain">
    % for terrain in terrains:
        <option value="{{terrain}}">{{terrain}}</option>
    % end
</select>

<p>
<select name="location">
    <option value="in_open">In the Open</option>
    <option value="in_fortress">In a fortress</option>
    <option value="in_city">In a city</option>
</select>
<p>

    <input type="checkbox" name="fortified" value="True"> The unit is fortified(makes no difference in a city, sentry instead)<br>

<p>
If in a city:<br>
        <input type="checkbox" name="greater_8" value="True"> Population &gt; 8<br>
        <input type="checkbox" name="walls" value="True"> Has city walls<br>
        <input type="checkbox" name="coastal" value="True"> Has coastal defence<br>
        <input type="checkbox" name="great_wall" value="True"> You have the Great Wall(which isn't obsolete)<br>

        <input type="checkbox" name="river" value="True"> Is on a river<br>



<p>
<input type="submit" value="Submit">


</form>


</body>
</html>
