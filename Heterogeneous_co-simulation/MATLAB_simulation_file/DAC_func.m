function [Xco2, X_res] = DAC_func(R_p,yCO2, P_ave, T, RH, e_voidage, Vpell, L, npell, nco2)
%Function takes in arguments and computes the conversion using shrinking
%model
%   Detailed explanation goes here
%R_p is pellet radius in m
%yCO2 is the mole fraction of CO2 in wet air stream from aspen plus simulations
%ntot is Total molar flow rate of wet air
%Vwet_air is  Volumetric flow rate of wet air
%RH is relative humidity of air from aspen
%eb  is  (Bed void fraction);
%Vcaco3 %flow rate from aspen in m^3/s
%L is the height of the column in meters
%P_ave is the average gas pressure in Pascals in the DAC unit,derived from Ergun's
%T is the operating temperature of the DAC unit in Kelvin

%% Time domain
t = linspace(0, 240*3600, 1000); % g hours, seconds

%% Parameters (Aspen/literature values)
rho_s = 30000; % mol/m^3 (solid molar density)
R = 8.314; % Gas constant J/(mol K)
C_CO2 = (yCO2 * P_ave) /(R * T); %mol/m^3 (DAC CO2 concentration)
eb = e_voidage;
%C_CO2 = 13;
k_g = 0.02; % m/s (gas film mass transfer coefficient)
k_r0 = 10^-5; % m/s (surface reaction rate constant)
D0 = 10^-11; %m/s (effective diffusivity through CaCO3 layer)
R_p = R_p / 2 ; %% Convert the diameter fed in to radius


%% Additional params
a = 10; n = 3;   % adjust based on best fit to literature
b = 5;  m = 2;   % softer effect on diffusivity

k_s_factor   = 1 + a*(RH.^n);      % scales reaction coefficient
D_eff_factor = 1 + b*(RH.^m);     % scales effective diffusivity

%% calculating the effective difusivity and the surface reation rate const
k_r    = k_r0  * k_s_factor;
D_eff = D0    * D_eff_factor;

%%
X = zeros(size(t));
t_surface = zeros(size(t));
t_reaction = zeros(size(t));
t_diffusion = zeros(size(t));


%% Time loop
for i = 1:length(t)
    %% Implicit function in x
    fun = @(X) ...
        (rho_s*R_p/(3*k_g*C_CO2))* X + ...
        ((rho_s*R_p)/(k_r*C_CO2))* (1 - (1 - X).^(1/3)) + ...
        ((rho_s*R_p^2)/(6*D_eff*C_CO2)) * ...
        (1 - 3*(1 - X).^(2/3) + 2*(1 - X)) ...
        - t(i);
    % Solve for conversion
    X(i) = fzero(fun, [0,1]);
    
    % store individual ressistance times
    t_surface(i) = ((rho_s*R_p)/(3*k_g*C_CO2)) * X(i);
    t_reaction(i) = ((rho_s*R_p)/(k_r*C_CO2)) * ...
        (1 - (1 - X(i))^(1/3));
    t_diffusion(i) = ((rho_s*R_p^2)/(6*D_eff*C_CO2)) * ...
        (1 - 3*(1 - X(i)).^(2/3) + 2*(1 - X(i)));
end

%%residence time calculations for MATLAB Conversion computing
%%Parameters definition

Vreactor = (pi * L * 7^2) /4; %volume of reactor

%% Vvoid calculations
Vvoid = (1-eb) * Vreactor; % Actual gas volume available
%% calculations of the residence time
t_res = (Vvoid)/Vpell;

%%Interpolating to calculate the conversion for a certain residence time t
X_res = interp1(t, X, t_res);

%% Calculating the equivalent conversion with respect to the CO2
Xco2 = X_res * npell  /nco2;
end