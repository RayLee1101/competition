import link, base64

from flask import Flask, request, jsonify

app = Flask(__name__)

cursor = link.conn.cursor()

## 餐廳crud
# 取得所有餐廳
@app.route("/get-restaurant", methods=["GET"])
def get_restaurant():
    cursor.execute("SELECT * from `restaurant`")
    rows = cursor.fetchall()
    return jsonify(rows)

# 新增餐廳
@app.route("/create_restaurant", methods=["POST"])
def create_restaurant():
    if(not request.form.get("name")):
        return jsonify("error")
    if(not request.form.get("address")):
        return jsonify("error")
    if(not request.form.get("phone")):
        return jsonify("error")
    if(not request.form.get("introduction")):
        return jsonify("error")
    
    name = request.form.get("name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    introduction = request.form.get("introduction")
    sql = "INSERT INTO `restaurant` (`id`, `name`, `address`, `phone`, `introduction`) VALUES (NULL, %s, %s, %s, %s)"
    value = (name, address, phone, introduction)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 更新餐廳
@app.route("/update_restaurant", methods=["PUT"])
def update_restaurant():
    if(not request.form.get("name")):
        return jsonify("error")
    if(not request.form.get("address")):
        return jsonify("error")
    if(not request.form.get("phone")):
        return jsonify("error")
    if(not request.form.get("introduction")):
        return jsonify("error")
    if(not request.args.get("id")):
        return jsonify("errir")

    name = request.form.get("name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    introduction = request.form.get("introduction")
    id = request.args.get("id")
    sql = "UPDATE `restaurant` SET `name` = %s, `address` = %s, `phone` = %s, `introduction` = %s WHERE `restaurant`.`id` = %s"
    value = (name, address, phone, introduction, id)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 刪除餐廳
@app.route("/delete_restaurant", methods=["DELETE"])
def delete_restaurant():
    if not request.args.get("id"):
        return jsonify("error")
    id = request.args.get("id")
    sql = "DELETE FROM restaurant WHERE `restaurant`.`id` = %s"
    value = (id, )
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")


## 菜單crud
# 取得菜單
@app.route("/get-menu", methods=["GET"])
def get_menu():
    if request.args.get("id"):
        sql = "SELECT * from `menu` WHERE `restaurant_id` = %s"
        value = (request.args.get("id"),)
        cursor.execute(sql, value)
    else:
        cursor.execute("SELECT * from `menu`")
    rows = cursor.fetchall()
    if rows:
        return jsonify(rows)
    else:
        return jsonify("error")
    
# 新增菜單
@app.route("/create-menu", methods=["POST"])
def create_menu():
    if not request.form.get("name"):
        return jsonify("error")
    if not request.form.get("price"):
        return jsonify("error")
    if not request.form.get("category"):
        return jsonify("error")
    if not request.files.get("image"):
        return jsonify("error")
    if not request.args.get("company_id"):
        return jsonify("error")
    
    name = request.form.get("name")
    price = request.form.get("price")
    category = request.form.get("category")
    image = request.files.get("image")
    company_id = request.args.get("company_id")

    image_bin = image.read()
    base64_encode = base64.b64encode(image_bin)
    base64_string = base64_encode.decode("utf-8")


    sql = "INSERT INTO `menu` (`id`, `name`, `price`, `category`, `image`, `company_id`) VALUES (Null,%s, %s, %s, %s, %s)"
    value = (name, price, category, base64_string, company_id)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 更新菜單
@app.route("/update-menu", methods=["PUT"])
def update_menu():
    if not request.args.get("id"):
        return jsonify("error")
    if not request.form.get("name"):
        return jsonify("error")
    if not request.form.get("price"):
        return jsonify("error")
    if not request.form.get("category"):
        return jsonify("error")
    if not request.files.get("image"):
        return jsonify("error")
    if not request.args.get("company_id"):
        return jsonify("error")
    
    id = request.args.get("id")
    name = request.form.get("name")
    price = request.form.get("price")
    category = request.form.get("category")
    image = request.files.get("image")
    company_id = request.args.get("company_id")
    

    image_bin = image.read()
    base64_encode = base64.b64encode(image_bin)
    base64_string = base64_encode.decode("utf-8")

    sql = "UPDATE `menu` SET `name` = %s, `price` = %s, `category` = %s, `image` = %s,`company_id` = %s WHERE `menu`.`id` = %s"
    value = (name, price, category, base64_string, company_id, id)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 刪除菜單
@app.route("/delete-menu", methods=["DELETE"])
def delete_menu():
    if not request.args.get("id"):
        return jsonify("error")
    id = request.args.get("id")
    sql = "DELETE FROM menu WHERE `menu`.`id` = %s"
    value = (id,)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

## 團購系統
# 新增團購
@app.route("/create_group", methods=["POST"])
def create_group():
    if not request.form.get("commodity_id"):
        return jsonify("error")
    if not request.form.get("user_id"):
        return jsonify("error")
    if not request.form.get("sum"):
        return jsonify("error")
    commodity_id = request.form.get("commodity_id")
    user_id = request.form.get("user_id")
    sum = request.form.get("sum")
    sql = "INSERT INTO `group_buy` (`id`, `commodity_id`, `user_id`, `sum`) VALUES (NULL, %s, %s, %s)"
    value = (commodity_id, user_id, sum)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 更新團購數量
@app.route("/update_group", methods=["PUT"])
def update_group():
    if not request.form.get("sum"):
        return jsonify("error")
    if not request.args.get("id"):
        return jsonify("error")
    id = request.args.get("id")
    sum = request.form.get("sum")
    sql = "UPDATE `group_buy` SET `sum` = %s WHERE `group_buy`.`id` = %s"
    value = (sum, id)
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 刪除團購
@app.route("delete_group", methods=["DELETE"])
def delete_group():
    if not request.args.get("id"):
        return jsonify("error")
    id = request.args.get("id")
    sql = "DELETE FROM group_buy WHERE `group_buy`.`id` = %s"
    value = (id, )
    cursor.execute(sql, value)
    link.conn.commit()
    return jsonify("success")

# 查詢商品的團購數量
@app.route("commodity_sum", methods=["GET"])
def commodity_sum():
    if not request.args.get("id"):
        return jsonify("error")
    id = request.args.get("id")
    sql = "SELECT * FROM `group_buy` where `commodity_id` = %s"
    value = (id, )
    cursor.execute(sql, value)
    rows = cursor.fetchall()
    sum = 0
    for r in rows:
        sum += r.sum
    return jsonify(sum)

# 查詢使用者所團購的商品及數量
@app.route("user_sum", methods=["GET"])
def user_sum():
    if not request.args.get("id"):
        return jsonify("error")
    id = request.args.get("id")
    sql = "SELECT * FROM `group_buy` where `user_id` = %s"
    value = (id, )
    cursor.execute(sql, value)
    rows = cursor.fetchall()
    return jsonify(rows)



if __name__ == '__main__':
    app.run(debug = True)
