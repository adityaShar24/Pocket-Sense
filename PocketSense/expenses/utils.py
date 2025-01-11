from decimal import Decimal
from django.core.exceptions import ValidationError

def handle_expense_split(expense_amount, split_type, splits_data):
    """
    Handle the splitting of an expense based on the split_type.
    
    Args:
        expense_amount (Decimal): The total amount of the expense.
        split_type (str): The type of split (e.g., 'equal', 'percentage', 'custom', etc.).
        splits_data (list): List of dictionaries with participant data (amounts, percentages, etc.).
    
    Returns:
        list: A list of dictionaries containing the participant data with their calculated amounts.
    
    Raises:
        ValidationError: If the split data is invalid or the amounts don't add up.
    """
    
    # Ensure the expense_amount is a Decimal for calculations
    expense_amount = Decimal(expense_amount)

    if not splits_data:
        raise ValidationError("No participants in the split.")
    
    # Common helper function to check if amounts are valid decimals
    def validate_amounts():
        for split in splits_data:
            if 'amount' not in split or not isinstance(split['amount'], (int, Decimal)):
                raise ValidationError("Each participant must have a valid amount.")

    # Handle 'equal' split type
    if split_type == 'equal':
        num_participants = len(splits_data)
        amount_per_participant = expense_amount / num_participants
        for split in splits_data:
            split['amount'] = amount_per_participant

    # Handle 'percentage' split type
    elif split_type == 'percentage':
        total_percentage = sum([split.get('percentage', 0) for split in splits_data])
        if total_percentage != 100:
            raise ValidationError("Total percentage does not sum up to 100.")
        
        for split in splits_data:
            percentage = Decimal(split.get('percentage', 0))
            split['amount'] = (percentage / Decimal(100)) * expense_amount

    # Handle 'custom' split type
    elif split_type == 'custom':
        total_custom_amount = sum([split.get('amount', 0) for split in splits_data])
        if total_custom_amount != expense_amount:
            raise ValidationError(f"Total custom amounts must sum to {expense_amount}.")
        
        for split in splits_data:
            if 'amount' not in split:
                raise ValidationError("Each participant must have a valid amount in the custom split.")

    # Handle 'proportional' split type
    elif split_type == 'proportional':
        total_factor = sum([split.get('factor', 0) for split in splits_data])
        if total_factor == 0:
            raise ValidationError("Total factor cannot be zero.")
        
        for split in splits_data:
            factor = Decimal(split.get('factor', 0))
            split['amount'] = (factor / total_factor) * expense_amount

    # Handle 'fixed_with_remainder' split type
    elif split_type == 'fixed_with_remainder':
        fixed_amount = sum([split.get('fixed_amount', 0) for split in splits_data])
        if fixed_amount >= expense_amount:
            raise ValidationError("Fixed amounts cannot exceed or equal the total expense.")
        
        remainder_amount = expense_amount - fixed_amount
        num_remainder_participants = len([split for split in splits_data if 'fixed_amount' not in split])
        
        if num_remainder_participants == 0:
            raise ValidationError("No participants to pay the remainder amount.")
        
        amount_per_remainder_participant = remainder_amount / num_remainder_participants
        for split in splits_data:
            if 'fixed_amount' not in split:
                split['amount'] = amount_per_remainder_participant
            else:
                split['amount'] = Decimal(split.get('fixed_amount', 0))

    # Raise error for unknown split type
    else:
        raise ValidationError(f"Unknown split type: {split_type}")

    # Validate amounts after calculation
    validate_amounts()

    return splits_data


def calculate_settlement(expenses, group_members):
    balances = {member: 0 for member in group_members}

    for expense in expenses:
        splits = expense.splits  
        paid_by = expense.paid_by.email
        amount = expense.amount

        balances[paid_by] += amount

        for split in splits:
            balances[split['email']] -= split['amount']

    settlements = []
    debtors = [(k, v) for k, v in balances.items() if v < 0]
    creditors = [(k, v) for k, v in balances.items() if v > 0]

    debtors.sort(key=lambda x: x[1])
    creditors.sort(key=lambda x: x[1], reverse=True)

    while debtors and creditors:
        debtor, debt_amount = debtors.pop(0)
        creditor, credit_amount = creditors.pop(0)

        settlement_amount = min(-debt_amount, credit_amount)
        settlements.append({
            "from": debtor,
            "to": creditor,
            "amount": settlement_amount
        })

        debt_amount += settlement_amount
        credit_amount -= settlement_amount

        if debt_amount < 0:
            debtors.insert(0, (debtor, debt_amount))
        if credit_amount > 0:
            creditors.insert(0, (creditor, credit_amount))

    return settlements