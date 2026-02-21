# Market Dynamics and Trading Simulation Framework

Implements a framework for simulating, analyzing, and learning about financial markets, trading strategies, and blockchain integration.

Currently v0.

## Project Structure

```
market_sim/
├── core/                      # Core functionality and base classes
│   ├── data/                 # Data management and storage
│   ├── models/              # Core market models and entities
│   └── utils/               # Utility functions and helpers
│
├── market/                   # Market simulation components
│   ├── exchange/            # Exchange mechanisms and matching engines
│   ├── agents/              # Trading agents and strategies
│   ├── mechanisms/          # Trading mechanisms (options, warrants, etc.)
│   └── dynamics/            # Market dynamics and price formation
│
├── strategies/               # Trading strategies implementation
│   ├── traditional/         # Classical trading strategies
│   ├── hft/                 # High-frequency trading strategies
│   └── ml/                  # Machine learning based strategies
│
├── simulation/              # Simulation framework
│   ├── engine/             # Simulation engine and time management
│   ├── scenarios/          # Pre-defined simulation scenarios
│   └── results/            # Results analysis and visualization
│
├── blockchain/              # Blockchain integration
│   ├── ethereum/           # Ethereum specific implementations
│   ├── consensus/          # Consensus mechanisms
│   └── contracts/          # Smart contracts
│
├── analysis/                # Analysis tools and utilities
│   ├── metrics/            # Performance and risk metrics
│   ├── visualization/      # Data visualization tools
│   └── reports/            # Report generation
│
├── api/                     # API interfaces
│   ├── rest/               # REST API
│   └── websocket/          # WebSocket API
│
├── ui/                      # User interfaces
│   ├── web/                # Web interface
│   ├── cli/                # Command-line interface
│   └── desktop/            # Desktop application
│
└── tests/                   # Test suite
    ├── unit/               # Unit tests
    ├── integration/        # Integration tests
    └── performance/        # Performance tests
```

## Features

### Market Simulation
- Real-time market simulation with configurable parameters
- Multiple asset types and trading mechanisms
- Price formation and order book management
- Trading agent framework with customizable strategies

### Trading Mechanisms
- Stock trading with various order types
- Options and warrants simulation
- Short selling and margin trading
- Custom mechanism creation framework

### High-Frequency Trading
- Ultra-low latency framework
- Order execution optimization
- Market making strategies
- Statistical arbitrage

### Blockchain Integration
- Ethereum smart contract integration
- Consensus mechanism simulation
- Cross-chain trading strategies
- DeFi protocol integration

### Learning Environment
- Interactive tutorials and scenarios
- Strategy backtesting framework
- Performance analytics
- Risk management tools

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run with coverage
pytest --cov=market_sim

# Run specific test file
pytest tests/integration/test_market_making.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Distributed Consensus Extension

### Concept Chosen

Inspired by the distributed consensus principles described in *Foundations of Distributed Consensus and Blockchains*, I implemented a simplified majority-based agreement mechanism within the market simulation engine.

Distributed consensus ensures that multiple nodes in a distributed system agree on a value even if some nodes may behave incorrectly or maliciously.

### Implementation

A new module `market_sim/consensus` was introduced:

- `ConsensusNode`: Simulates an independent validator node.
- `MajorityConsensus`: Implements a majority voting mechanism.

Before committing a trade in the matching engine:

1. A trade is created.
2. The trade is validated by multiple simulated nodes.
3. Each node independently verifies:
   - Quantity > 0
   - Price > 0
   - Buyer and seller are different
4. The trade is accepted only if a majority of nodes approve it.

This models a simplified quorum-based consensus mechanism integrated directly into the trade creation flow.

### Design Rationale

The consensus layer was introduced at the trade creation boundary (`_create_trade`) to ensure validation occurs before state mutation. This preserves modularity and clean separation of concerns while demonstrating distributed agreement principles.

### Future Improvements

- Introduce Byzantine (malicious) nodes.
- Simulate network latency between validators.
- Implement leader-based consensus (e.g., Raft-style protocol).
- Extend toward blockchain-style trade logging.
