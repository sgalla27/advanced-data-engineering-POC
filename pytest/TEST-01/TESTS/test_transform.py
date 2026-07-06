import pandas as pd
from transform import standardize_status, calculate_claim_ratio

def test_standardize_status():
    df = pd.DataFrame({'status': ['open','Closed','PENDING']
    })
    
    result = standardize_status(df)

    assert result['status'].tolist() == ['OPEN', 'CLOSED', 'PENDING']

def test_calculate_claim_ratio():
    df = pd.DataFrame({'amount':[5000.0],
                       'premium':[10000.0]
    })

result = calculate_claim_ratio(df)

assert result['claim_ratio'].iloc[0] == 0.5