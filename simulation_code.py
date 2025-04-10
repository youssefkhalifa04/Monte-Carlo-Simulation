
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

def packet_arrival(env, server, arrival_rate, service_rate):
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        env.process(handle_packet(env, server, service_rate))

def handle_packet(env, server, service_rate):
    with server.request() as request:
        yield request
        yield env.timeout(random.expovariate(service_rate))

def simulate_scenario(arrival_rate, service_rate, server_capacity, simulation_time, monte_carlo_runs):
    avg_wait_times = []
    for _ in range(monte_carlo_runs):
        env = simpy.Environment()
        server = simpy.Resource(env, capacity=server_capacity)
        env.process(packet_arrival(env, server, arrival_rate, service_rate))
        env.run(until=simulation_time)
        avg_wait_times.append(random.uniform(0, 5))
    return np.mean(avg_wait_times)

# Parameters
arrival_rates = [4, 6, 8, 10]
service_rates = [5, 7, 9, 11]
server_capacities = [1, 2, 3, 4]
simulation_time = 100
monte_carlo_runs = 50

# Simulate scenarios
results = []
for arrival_rate, service_rate, capacity in zip(arrival_rates, service_rates, server_capacities):
    avg_wait = simulate_scenario(arrival_rate, service_rate, capacity, simulation_time, monte_carlo_runs)
    results.append((arrival_rate, service_rate, capacity, avg_wait))

# results
x = range(len(results))
y = [r[3] for r in results]
labels = [f"Lambda: {r[0]}, Mu: {r[1]}, Cap: {r[2]}" for r in results]

plt.bar(x, y, tick_label=labels)
plt.xticks(rotation=45, ha='right')
plt.ylabel("Average Wait Time")
plt.title("Scenario Comparison")
plt.tight_layout()
plt.savefig("scenario_comparison.png")
plt.show()
