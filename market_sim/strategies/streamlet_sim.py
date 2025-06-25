import random
from collections import defaultdict

class StreamletNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.chain = []
        self.votes = defaultdict(list)

    def vote(self, round_number, block):
        self.votes[round_number].append(block)
        return (self.node_id, round_number, block)

class StreamletSimulation:
    def __init__(self, total_nodes=4, total_rounds=5):
        self.nodes = [StreamletNode(i, total_nodes) for i in range(total_nodes)]
        self.total_nodes = total_nodes
        self.total_rounds = total_rounds
        self.chain = []

    def run(self):
        for round_number in range(1, self.total_rounds + 1):
            leader_id = round_number % self.total_nodes
            block = f"Block_R{round_number}_L{leader_id}"
            print(f"\n[Round {round_number}] Leader is Node {leader_id}, proposes {block}")

            votes = [node.vote(round_number, block) for node in self.nodes]

            vote_count = defaultdict(int)
            for _, _, voted_block in votes:
                vote_count[voted_block] += 1

            for block_val, count in vote_count.items():
                if count >= (2 * self.total_nodes) // 3:
                    print(f"✔️ Block '{block_val}' is notarized with {count} votes")
                    self.chain.append(block_val)
                    break
            else:
                print(f"❌ No block notarized this round")

        print("\n🏁 Final Chain:")
        for b in self.chain:
            print(f" - {b}")

# Run the simulation if this file is executed directly
if __name__ == "__main__":
    sim = StreamletSimulation()
    sim.run()
