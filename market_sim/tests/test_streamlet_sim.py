import unittest
from market_sim.strategies.streamlet_sim import StreamletSimulation

class TestStreamletSimulation(unittest.TestCase):
    def test_chain_length(self):
        sim = StreamletSimulation(total_nodes=4, total_rounds=5)
        sim.run()
        self.assertEqual(len(sim.chain), 5)

    def test_block_naming(self):
        sim = StreamletSimulation(total_nodes=4, total_rounds=3)
        sim.run()
        self.assertTrue(all("Block_R" in b for b in sim.chain))

if __name__ == "__main__":
    unittest.main()
