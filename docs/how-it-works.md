# Overview of the Package

This package facilitates the extraction and evaluation of metrics from various sources. It consists of connectors for establishing connections and deducers for data handling and metric extraction. The deduced metrics are either boolean values or numerical.

## Components

### Authenticators
- Abstract base class: `Authenticator`
- **Derived Classes:**
    - `BearerTokenAuthenticator`: Implements bearer token authentication.
    - `TokenAuthenticator`: Uses token-based authentication.
    - `UserPasswordBasicAuthenticator`: Provides basic authentication via username and password.



### Client
- **Abstract Base Class:** `Client`.
- **Key Features:**
    - Maintains configuration settings.
    - Includes an abstract method `make_request` for making requests to endpoints.


### Connector
- **Abstract Base Class:** `Connector`.
- **Key Features:**
    - Manages a `Client` instance.
    - Has an abstract method `ensure_connectivity` for ensuring the connection.

### Deducer
- **Abstract Base Class:** `Deducer`.
- **Key Features:**
    - Utilizes `Connector` for data retrieval.
    - Includes abstract methods `retrieve_data`, `process_data`, and `finalize`.
    - The `deduce` method orchestrates the retrieval, processing, and finalizing of data into a metric.

### Metric
- **Class:** `Metric`.
- **Key Features:**
    - Stores values that are integers, floats, or booleans.
    - Includes methods `satisfies` and `satisfies_all` for criteria evaluation.


## Process Flow

## Process Flow

1. **Authentication:** Selection and instantiation of an `Authenticator` based on the required authentication method.
2. **Connection Establishment:** Creation and utilization of a `Connector` with a `Client` to ensure connectivity.
3. **Data Extraction and Processing:** Initialization of a `Deducer` to manage data retrieval, processing, and finalizing.
4. **Metric Evaluation:** Use of the `Metric` class for storing and evaluating the final values against set criteria.
