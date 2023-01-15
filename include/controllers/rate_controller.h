#ifndef RATE_CONTROLLER_H
#define RATE_CONTROLLER_H

#include <quadrotor_model.h>
#include <controllers/pid.h>
#include <eigen3/Eigen/Eigen>

namespace mrs_multirotor_simulator
{

class RateController {

public:
  struct Params
  {
    int n_motors;
    double          kp;
    double          kd;
    double          ki;
    double          force_coef;
    double          max_rpm;
    double          min_rpm;
    Eigen::MatrixXd allocation_matrix;
  };

  struct Reference
  {
    Eigen::Vector3d angular_rate;
    double          throttle;
  };

  RateController();

  void setParams(const Params& params);

  Eigen::VectorXd getControlSignal(const QuadrotorModel::State& state, const RateController::Reference& reference, const double& dt);

private:
  Params params_;

  PIDController pid_x_;
  PIDController pid_y_;
  PIDController pid_z_;
};

}  // namespace mrs_multirotor_simulator

#endif  // RATE_CONTROLLER_H
