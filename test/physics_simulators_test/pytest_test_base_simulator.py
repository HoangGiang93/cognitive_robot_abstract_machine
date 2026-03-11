#!/usr/bin/env python3

import time
import pytest
from typing import Optional, List

import numpy

from physics_simulators.base_simulator import (
    BaseSimulator,
    SimulatorState,
    SimulatorConstraints,
    SimulatorStopReason,
    SimulatorCallback,
    SimulatorCallbackResult,
)


class TestBaseSimulator:
    file_path: str = ""
    world_path: str = ""
    robots_path: Optional[str] = None
    headless: bool = False
    step_size: float = 1e-3
    Simulator = BaseSimulator
    number_of_envs: int = 1

    # ----------- Test 1: Initialize Simulator -----------
    def test_initialize_simulator(self):
        simulator = self.Simulator(
            file_path=self.file_path,
            world_path=self.world_path,
            robots_path=self.robots_path,
            headless=self.headless,
            step_size=self.step_size,
            number_of_envs=self.number_of_envs,
        )
        assert simulator.state is SimulatorState.STOPPED
        assert simulator.headless is self.headless
        assert simulator.stop_reason is None
        assert simulator.simulation_thread is None

    # ----------- Test 2: Start and Stop Simulator -----------
    def test_start_and_stop_simulator(self):
        simulator = self.Simulator()
        simulator.start(simulate_in_thread=False)
        assert simulator.state is SimulatorState.RUNNING
        simulator.stop()
        assert simulator.state is SimulatorState.STOPPED
        assert simulator.stop_reason is SimulatorStopReason.STOP
        assert not simulator.renderer.is_running()
        if simulator.simulation_thread:
            assert not simulator.simulation_thread.is_alive()

    # ----------- Test 3: Pause and Unpause Simulator -----------
    def test_pause_and_unpause_simulator(self):
        simulator = self.Simulator()
        simulator.start(simulate_in_thread=False)
        simulator.pause()
        assert simulator.state is SimulatorState.PAUSED
        simulator.unpause()
        assert simulator.state is SimulatorState.RUNNING
        simulator.stop()

    # ----------- Test 4: Step Simulator -----------
    def test_step_simulator(self):
        simulator = self.Simulator()
        simulator.start(simulate_in_thread=False)
        assert simulator.stop_reason is None
        for i in range(10):
            assert simulator.current_number_of_steps == i
            assert abs(simulator.current_simulation_time - i * simulator.step_size) < 1e-6
            simulator.step()
            assert simulator.stop_reason is None
        simulator.stop()
        assert simulator.stop_reason is SimulatorStopReason.STOP
        if simulator.simulation_thread:
            assert not simulator.simulation_thread.is_alive()

    # ----------- Test 5: Reset Simulator -----------
    def test_reset_simulator(self):
        simulator = self.Simulator()
        simulator.start(simulate_in_thread=False)
        simulator.reset()
        assert simulator.current_number_of_steps == 0
        assert simulator.current_simulation_time == 0.0
        simulator.stop()
        assert simulator.stop_reason is SimulatorStopReason.STOP

    # ----------- Test 6: Real-time Constraint -----------
    def test_real_time(self):
        self.step_size = 1e-4
        simulator = self.Simulator()
        constraints = SimulatorConstraints(max_real_time=1.0)
        simulator.start(constraints=constraints, simulate_in_thread=True)
        while simulator.state == SimulatorState.RUNNING:
            time.sleep(1)
        assert simulator.state is SimulatorState.STOPPED

    # ----------- Test 7: Callbacks -----------
    def test_making_functions(self):
        result_1 = SimulatorCallbackResult(
            type=SimulatorCallbackResult.ResultType.SUCCESS_WITHOUT_EXECUTION,
            info="Test function 1",
            result="Hello, World!",
        )

        def function_1(sim: BaseSimulator) -> SimulatorCallbackResult:
            return result_1

        function_1_cb = SimulatorCallback(function_1)

        result_2 = SimulatorCallbackResult(
            type=SimulatorCallbackResult.ResultType.FAILURE_AFTER_EXECUTION_ON_DATA,
            info="Test function 2",
            result="Hello, World!",
        )

        def function_2(sim: BaseSimulator) -> SimulatorCallbackResult:
            return result_2

        function_2_cb = SimulatorCallback(function_2)

        simulator = self.Simulator(callbacks=[function_1_cb, function_2_cb])
        assert simulator.callbacks["function_1"]() == result_1
        assert simulator.callbacks["function_2"]() == result_2

        with pytest.raises(Exception) as e:
            self.Simulator(callbacks=[function_1_cb, function_2_cb, function_2_cb])
        assert f"Function {function_2_cb.__name__} is already defined" in str(e.value)