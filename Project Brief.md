# Project Brief: Autonomous Puzzle-Solving Robotic Arm with Dual-Arm Teleoperation

## Project Title
**PuzzArm: AI-Powered Robotic Solver for Children's Number Puzzle**

## Project Overview
This project develops a stationary robotic system using a Hiwonder xArm1S 6-DOF arm mounted on a Jetson Nano to autonomously solve a wooden number puzzle (0-9 pieces with fruit patterns). The system integrates computer vision for piece detection and slot matching, ML-driven pose estimation and imitation learning for grasping/placement, and ROS2 for control. A novel dual-arm teleoperation feature uses a second identical xArm1S as a "master" to intuitively demonstrate and record motions for the "slave" arm, accelerating ML training data collection. The end goal is a demo-ready prototype capable of solving the puzzle with 90%+ success rate, handling arbitrary piece orientations, in under 5 minutes per solve.

**Primary Objective**: Create an educational robotics platform blending CV, ML, and teleop for puzzle manipulation, adaptable to similar tasks (e.g., sorting games).

**Secondary Objectives**:
- Enable human-in-the-loop teleop for intuitive control and data gathering.
- Achieve real-time performance (~10-15 FPS detection, <100ms motion inference) on Jetson Nano hardware.

**Stakeholders**: Project lead (user/developer); potential extensions for educational demos or open-source contributions.

## Scope
### In-Scope
- Hardware integration: Single-arm stationary setup (Jetson Nano + xArm1S + top-down CSI camera); dual-arm teleop mirroring.
- Software: ROS2-based pipeline for detection, pose estimation, grasp planning, and motion execution.
- ML Components: YOLOv11-nano for detection/classification; PCA/DOPE for 2D pose; ResNet18+LSTM policy for imitation learning from teleop demos.
- Puzzle-Specific: Detect loose pieces/slots, match numbers (e.g., "loose_3" to "empty_slot_3"), handle rotations via augmented training.
- Testing: 20-50 teleop demos per piece; end-to-end success metrics on varied orientations/lighting.
- Documentation: Code repo (GitHub fork of xArm/JetBot), setup guide, ML training scripts.

### Out-of-Scope
- JetBot mobility (stationary only).
- Advanced grippers (assumes parallel-jaw identical on both arms; no suction/force sensing).
- Multi-puzzle generalization (focus on this 0-9 set).
- Production deployment (prototype for lab/home use).

## Hardware Requirements
| Component | Details | Quantity | Notes |
|-----------|---------|----------|-------|
| Jetson Nano | Developer Kit (from JetBot) with JetPack 5.x | 2 (one per arm) | For parallel master/slave operation; shared if using USB hub. |
| xArm1S Robotic Arm | 6-DOF, LewanSoul servos, serial TTL control | 2 | Identical grippers (parallel-jaw); ~1A power draw each. |
| Camera | CSI top-down mount (e.g., Raspberry Pi Cam v2) | 1 (on slave arm) | Fixed overhead view; calibrate intrinsics once. |
| Power | 5V/3A+ PSU or powered USB hub | 1 | To handle dual arms; monitor servo voltages. |
| Misc | Puzzle board/pieces, ArUco markers for calibration, serial cables (TTL/USB adapters) | As needed | Total est. cost: $500-800 (assuming existing JetBot/xArm). |

## Software Stack
- **OS/Platform**: Ubuntu 20.04/22.04 on Jetson Nano (JetPack 5.x).
- **Core Framework**: ROS2 Humble/Iron (nodes for serial control, TF transforms, MoveIt2 planning).
- **CV/ML Libraries**: OpenCV, Ultralytics YOLOv11, PyTorch (TensorRT export), isaac_ros_pose_estimation.
- **Control**: Custom Python serial wrapper for xArm (joint positions/voltages); rclpy for ROS2 nodes.
- **Tools**: Jupyter for training; ROS2 bags for demo recording; RViz2 for visualization.
- **Version Control**: GitHub repo with branches for hardware, vision, teleop, and ML.

## Key Technical Approach
1. **Perception**: Top-down camera → YOLOv11-nano detects pieces/slots → PCA for 2D pose (x,y,θ) handling rotations.
2. **Teleoperation**: Master arm publishes `/master_joints` (JointState) → Slave subscribes and mirrors via serial; record image-joint pairs for ML.
3. **Motion Control**: Imitation learning policy (ResNet18+LSTM) trained on teleop data → Outputs joint deltas for pick (grasp peg offset), lift, transfer, place (align θ).
4. **Execution Loop**: Detect → Match → Policy inference → Serial commands → Verify (re-detect post-place).
5. **Fallback**: MoveIt2 IK for recovery if policy fails.

**Data Pipeline**: 1-5k samples from 50 teleop cycles; train ~30 min on Nano.

## Milestones & Timeline
Assuming 1-2 developers, part-time (10-15 hrs/week); total est. 4-6 weeks from kickoff (target: mid-November 2025).

| Milestone | Description | Deliverables | Est. Duration |
|-----------|-------------|--------------|---------------|
| 1: Setup & Integration | Hardware wiring, ROS2 workspace, basic serial nodes. | Working single-arm teleop; dual-arm mirroring demo. | Week 1 |
| 2: Perception | YOLO training/annotation; pose estimation node. | 90% detection accuracy on static images. | Week 2 |
| 3: Teleop & Data Collection | Master-slave sync; ROS2 bag recording. | 50+ demo trajectories saved. | Week 2-3 |
| 4: ML Policy | Train/export imitation learner; integrate with ROS2. | End-to-end pick-place for 3-5 pieces (80% success). | Week 3-4 |
| 5: Full Autonomy & Testing | Loop integration, error handling, benchmarks. | Complete puzzle solve video; 90% success on full set. | Week 4-5 |
| 6: Polish & Doc | Refinements, repo setup, user guide. | GitHub release; demo script. | Week 5-6 |

## Risks & Mitigation
- **Risk**: Serial latency/jitter → Motion desync. *Mitigation*: 10Hz loops; buffer commands.
- **Risk**: ML data quality (e.g., poor rotations). *Mitigation*: Augment datasets; start with 10 demos per piece.
- **Risk**: Jetson overheating/underpower. *Mitigation*: Heatsink/fan; separate PSUs.
- **Risk**: Gripper slips on pegs. *Mitigation*: Fixed offsets + vision verification; test 20x per config.
- **Assumptions**: Familiarity with ROS2/Python; access to GitHub/NVIDIA forums for troubleshooting.

## Resources Needed
- **Team**: 1 lead dev (you); optional mentor for ML tuning.
- **Budget**: <$200 (cables, hub, markers).
- **Support**: NVIDIA Jetson forums; ROS Discourse; Hiwonder GitHub issues.
- **Success Metrics**: 90% solve rate; <5s per piece; open-source potential (e.g., 100+ stars on repo).

This brief provides a roadmap to transform your dual-arm setup into a cutting-edge puzzle solver. Ready to iterate—feedback on timeline or scope?