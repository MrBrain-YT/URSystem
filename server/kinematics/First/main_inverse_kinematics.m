function [ Inv_kin_result ] = main_inverse_kinematics(x1, y1)
    clc

    %%% This example shows how to do the inverse kinematics for a 4 link
    %%% manipulator
    
    % DH parameters
    global d1 a1 alpha1 
    global d2 a2 alpha2
    global d3 a3 alpha3
    global d4 a4 alpha4 
    global x_des y_des z_des %where you want the end-effector
    
    
    %D-H for links. Theta's are not set, because we need to find them. 
    d1=0; a1=0;  alpha1=0; % theta1
    d2=0; a2=195; alpha2=0; % theta2
    d3=0; a3=235; alpha3=0; %theta3
    d4=0; a4=65; alpha4=0; %theta4
    
    
    %Below is the input given to the IK
    %Location where we want the end-effector to be
    %Change this value if you want to try out different position
    x_des = x1; y_des = y1; z_des = 0;
    
    % initial guess values for theta
    theta1=0; theta2=0; theta3=0; theta4=0;
    
    X0 = [theta1, theta2, theta3, theta4];
    
    
    %fsolve solves for the roots for the equation X-XDES
    [X,FVAL,EXITFLAG] = fsolve('find_joint_angles',X0);
    theta1 = X(1);
    theta2 = X(2);
    theta3 = X(3);
    theta4 = X(4);
    disp([theta1, theta2, theta3, theta4])
    disp(['Exitflag after running fsolve = ', num2str(EXITFLAG) ]) %Tells if fsolve converged or not
                   %1 means converged else not converged             
                  
     X;
     FVAL;
    %Visualise the manipulator with the generated theta values
    X_des = [x_des y_des,z_des];
    
    Inv_kin_result = plot_manipulator(X,X_des);
end