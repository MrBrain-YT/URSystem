function angle = calculateAngle(x1_start, y1_start, z1_start, x1_end, y1_end, z1_end, x2_end, y2_end, z2_end)
    % Вычисление векторов направления линий
    vector1 = [x1_end - x1_start, y1_end - y1_start, z1_end - z1_start];
    vector2 = [x2_end - x1_end, y2_end - y1_end, z2_end - z1_end];

    % Вычисление скалярного произведения
    dotProduct = dot(vector1, vector2);

    % Вычисление длин векторов
    length1 = norm(vector1);
    length2 = norm(vector2);

    % Вычисление угла в радианах
    angle = acos(dotProduct / (length1 * length2));

    % Определение направления угла
    crossProduct = cross(vector1, vector2);
    if crossProduct(3) < 0
        angle = -angle;
    end

    % Преобразование угла в градусы
    angle = rad2deg(angle);
end
