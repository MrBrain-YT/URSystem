%%%This function is used to animate/plot the manipulator

function [res] = plot_manipulator(X0,X_des)
    theta1=X0(1); theta2=X0(2); theta3=X0(3); theta4=X0(4);
    
    global d1 a1 alpha1 
    global d2 a2 alpha2
    global a3 d3  alpha3 
    global a4 d4 alpha4 
    
    % Now let us plot the results.
    H01 = DH(a1,alpha1,d1,theta1); 
    H12 = DH(a2,alpha2,d2,theta2); 
    H23 = DH(a3,alpha3,d3,theta3); 
    H34 = DH(a4,alpha4,d4,theta4);
    
    
    %Location of joint 1
    endOfLink1 = H01(1:3,4);
    
    %Location of joint 2
    H02 = H01*H12;
    endOfLink2 = H02(1:3,4);
    
    %Location of joint 3
    H03 = H02*H23;
    endOfLink3 = H03(1:3,4);
    
    %Location of joint 4
    H04 = H03*H34;
    endOfLink4 = H04(1:3,4);
    
    ang2 = calculateAngle(0,50,0,0,0,0,endOfLink2(1),endOfLink2(2),0);
    ang3 = calculateAngle(endOfLink1(1),endOfLink1(2),0,endOfLink2(1),endOfLink2(2),0,endOfLink3(1),endOfLink3(2),0);
    ang4 = calculateAngle(endOfLink2(1),endOfLink2(2),0,endOfLink3(1),endOfLink3(2),0,endOfLink4(1),endOfLink4(2),0);
    res = [ang2, ang3, ang4];
end

