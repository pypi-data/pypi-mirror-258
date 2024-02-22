# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = [
        "mrp.production",
        "mixin.policy",
    ]

    def _compute_policy(self):
        _super = super(MrpProduction, self)
        _super._compute_policy()

    @api.depends(
        "state",
        "move_finished_ids.stock_valuation_layer_ids",
    )
    def _compute_stock_valuation_id(self):
        for rec in self:
            stock_valuation_id = self.env["stock.valuation.layer"].search(
                [("stock_move_id", "in", rec.move_finished_ids.ids)], limit=1
            )
            rec.stock_valuation_id = stock_valuation_id.id

    @api.depends("stock_valuation_id.unit_cost")
    def _compute_unit_cost(self):
        for rec in self:
            rec.unit_cost = rec.stock_valuation_id.unit_cost

    @api.depends("stock_valuation_id.value")
    def _compute_value(self):
        for rec in self:
            rec.value = rec.stock_valuation_id.value

    type_id = fields.Many2one(
        comodel_name="mrp_production_type",
        string="Type",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    date_backdating = fields.Datetime(
        string="Actual Movement Date",
    )
    validate_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        compute_sudo=True,
    )
    mark_done_ok = fields.Boolean(
        string="Can Mark as Done",
        compute="_compute_policy",
        compute_sudo=True,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        compute_sudo=True,
    )
    plan_ok = fields.Boolean(
        string="Can Plan",
        compute="_compute_policy",
        compute_sudo=True,
    )
    unplan_ok = fields.Boolean(
        string="Can Unplan",
        compute="_compute_policy",
        compute_sudo=True,
    )
    check_availability_ok = fields.Boolean(
        string="Can Check availability",
        compute="_compute_policy",
        compute_sudo=True,
    )
    unreserve_ok = fields.Boolean(
        string="Can Unreserve",
        compute="_compute_policy",
        compute_sudo=True,
    )
    scrap_ok = fields.Boolean(
        string="Can Scrap",
        compute="_compute_policy",
        compute_sudo=True,
    )
    lock_ok = fields.Boolean(
        string="Can Lock",
        compute="_compute_policy",
        compute_sudo=True,
    )
    unlock_ok = fields.Boolean(
        string="Can Unlock",
        compute="_compute_policy",
        compute_sudo=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        compute_sudo=True,
    )
    cancel_confirm_ok = fields.Boolean(
        string="Can Cancel (Confirmation)",
        compute="_compute_policy",
        compute_sudo=True,
    )
    unbuild_ok = fields.Boolean(
        string="Can Unbuild",
        compute="_compute_policy",
        compute_sudo=True,
    )
    stock_valuation_id = fields.Many2one(
        comodel_name="stock.valuation.layer",
        string="Stock Valuation",
        compute="_compute_stock_valuation_id",
        compute_sudo=True,
        store=True,
    )
    unit_cost = fields.Float(
        string="Unit Value", compute="_compute_unit_cost", compute_sudo=True, store=True
    )
    value = fields.Float(
        string="Total Value", compute="_compute_value", compute_sudo=True, store=True
    )

    @api.constrains("date_backdating")
    def _check_date_backdating(self):
        now = fields.Datetime.now()
        for move in self:
            if move.date_backdating and move.date_backdating > now:
                raise UserError(
                    _("You can not process an actual " "movement date in the future.")
                )

    def button_mark_done(self):
        for rec in self:
            rec.move_finished_ids.write(
                {
                    "date_backdating": rec.date_backdating,
                }
            )
        return super(MrpProduction, self).button_mark_done()

    @api.model
    def _get_policy_field(self):
        res = super(MrpProduction, self)._get_policy_field()
        policy_field = [
            "validate_ok",
            "mark_done_ok",
            "confirm_ok",
            "plan_ok",
            "unplan_ok",
            "check_availability_ok",
            "unreserve_ok",
            "scrap_ok",
            "lock_ok",
            "unlock_ok",
            "cancel_ok",
            "cancel_confirm_ok",
            "unbuild_ok",
        ]
        res += policy_field
        return res
