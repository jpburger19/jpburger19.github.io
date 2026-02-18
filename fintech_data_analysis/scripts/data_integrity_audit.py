import pandas as pd

def reconcile_payments(internal_ledger_path, bank_statement_path):
    """
    Identifies 'Orphan Transactions'—money that exists in one system but not the other.
    Essential for Fintech Support and Finance operations.
    """
    ledger = pd.read_csv(internal_ledger_path)
    bank = pd.read_csv(bank_statement_path)

    # Outer join to find missing records on either side
    recon_df = pd.merge(ledger, bank, on='transaction_ref', how='outer', indicator=True)

    # Identify discrepancies
    missing_in_bank = recon_df[recon_df['_merge'] == 'left_only']
    missing_in_ledger = recon_df[recon_df['_merge'] == 'right_only']

    # Log results for the Support/Operations team
    print(f"Reconciliation Summary:")
    print(f"- Ledger entries missing from Bank: {len(missing_in_bank)}")
    print(f"- Bank entries missing from Ledger: {len(missing_in_ledger)}")
    
    return missing_in_bank, missing_in_ledger