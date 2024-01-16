function [ fwd_kin_result ] = Main_Fwd_Kinematics(t1, t2,t3, t4)
    % Denavit-Hartenberg parameters


    % Denavit-Hartenberg parameters matrix
    dh_params = [t1      t2    t3    t4;    % theta
                 0          0         0         0;         % d
                 0           195        235        65;        % r
                 90      0         0         0];        % alpha

    % Compute forward kinematics
    fwd_kin_result = Calc_Fwd_Kinematics(dh_params);

end

