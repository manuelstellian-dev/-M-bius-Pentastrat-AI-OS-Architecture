package mobius.safety

# Default deny
default allow = false

# Allow deployment only if all safety measures are in place
allow {
  input.action == "deploy"
  input.artifact.attested == true
  input.change.canary == true
  input.change.rollback_plan_defined == true
}

# Entropy budget constraint
entropy_allowed {
  input.action == "set_entropy"
  input.value <= 0.05
}

# Regen budget constraint
regen_allowed {
  input.action == "set_regen"
  input.value <= 0.10
}

# High risk changes require all safety measures
high_risk_deploy {
  input.action == "deploy"
  input.risk_level == "high"
  input.artifact.attested == true
  input.change.canary == true
  input.change.rollback_plan_defined == true
  input.change.safety_verified == true
}
