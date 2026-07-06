import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import pandas as pd
from transform import standardize_status, calculate_claim_ratio, add_high_risk_flag, drop_null_policy_id




def test_standardize_status():
    df = pd.DataFrame({
        'status': ['open', 'Closed', 'PENDING']
    })

    result = standardize_status(df)

    assert result['status'].tolist() == [
        'OPEN',
        'CLOSED',
        'PENDING'
    ]


def test_calculate_claim_ratio():
    df = pd.DataFrame({
        'amount': [5000.0],
        'premium': [10000.0]
    })

    result = calculate_claim_ratio(df)

    assert result['claim_ratio'].iloc[0] == 0.5


def test_high_risk_flag():
    df = pd.DataFrame({
        "claim_ratio": [0.8]
    })

    result = add_high_risk_flag(df)

    assert result["is_high_risk"].iloc[0] == True


def test_null_policy_id_dropped():
    df = pd.DataFrame({
        "policy_id": [1, None],
        "amount": [500, 300]
    })

    result = drop_null_policy_id(df)

    assert len(result) == 1