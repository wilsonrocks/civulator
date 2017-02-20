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

Location:
<select name="location">
    <option value="open">Out in the Open</option><br>
    <option value="city">In a City</option><br>
    <option value="fort">In a Fort</option>
</select>
    <p>

<input type="checkbox" name="river" value="True">On a river<br>
<input type="checkbox" name="fortified" value="True">Fortified<br>
<p>

<input type="submit" value="Submit">


</form>
</body>
</html>
