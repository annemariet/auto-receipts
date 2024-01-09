def fill_missing_columns(input_df, columns_to_add, default_value="", default_type=str):
    for col in columns_to_add:
        if col not in input_df.columns:
            input_df[col] = default_value
            input_df[col] = input_df[col].astype(default_type)
        else:
            input_df[col] = input_df[col].fillna(default_value).astype(default_type)
    return input_df


def autocorrect_phone(input_value):
    number = "0" + str(input_value).lstrip("0").replace(".0", "")
    if len(number) < 10:
        number += "0"
    number = " ".join((number[2 * s : 2 * s + 2] for s in range(5)))
    return number


def autocorrect(input_df):
    input_df["Line_Amount"] = input_df["Line_Amount"].apply(
        lambda x: x.strip("€ *") if isinstance(x, str) else x
    )

    input_df["Price"] = input_df["Price"].apply(
        lambda x: x.replace("/kg", "").replace("/ kg", "").strip("€ *")
        if isinstance(x, str)
        else x
    )

    input_df["Merchant_Phone"] = input_df["Merchant_Phone"].apply(autocorrect_phone)
